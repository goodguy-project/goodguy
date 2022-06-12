//go:build darwin || linux

package util

import (
	"fmt"
	"io/ioutil"
	"math/rand"
	"os"
	"os/exec"
	"time"
)

func RunCmd(cmd string, args ...interface{}) string {
	cmd = fmt.Sprintf(cmd, args...)
	_ = os.Mkdir(".tmp", 0666)
	fileName := fmt.Sprintf("./.tmp/%v-%v.sh", time.Now().Unix(), rand.Int31())
	err := ioutil.WriteFile(fileName, []byte(cmd), 0600)
	if err != nil {
		panic(err)
	}
	command := exec.Command("sh", fileName)
	output, _ := command.CombinedOutput()
	return string(output)
}
