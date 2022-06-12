//go:build windows

package util

import (
	"fmt"
	"io/ioutil"
	"math/rand"
	"os"
	"os/exec"
	"time"
)

func init() {
	rand.Seed(time.Now().UnixNano())
}

func RunCmd(cmd string, args ...interface{}) string {
	cmd = fmt.Sprintf(cmd, args...)
	cmd = "@echo off\n" + cmd
	_ = os.Mkdir(".tmp", 0666)
	fileName := fmt.Sprintf(".\\.tmp\\%v-%v.bat", time.Now().Unix(), rand.Int31())
	err := ioutil.WriteFile(fileName, []byte(cmd), 0600)
	if err != nil {
		panic(err)
	}
	command := exec.Command("cmd", "/c", fileName)
	output, _ := command.CombinedOutput()
	fmt.Println(string(output))
	return string(output)
}
