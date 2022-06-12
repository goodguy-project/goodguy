package util

import (
	"fmt"
	"testing"
)

func Test_RunCmd(t *testing.T) {
	fmt.Println(RunCmd(`docker ps -a -q --filter="name=goodguy-mysql"`))
}
