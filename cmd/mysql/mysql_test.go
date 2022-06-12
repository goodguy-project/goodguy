package mysql

import (
	"fmt"
	"testing"
)

func Test_GetNameId(t *testing.T) {
	s := GetNameId()
	fmt.Printf("id=|%s|\n", s)
}

func Test_Stop(t *testing.T) {
	Stop()
}

func Test_Clean(t *testing.T) {
	Clean()
}

func Test_Backup(t *testing.T) {
	Backup()
}

func Test_Run(t *testing.T) {
	Deploy("")
}
