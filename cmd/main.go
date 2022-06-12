package main

import (
	"fmt"
	"os"
	"sync"
	"time"

	"github.com/goodguy-project/goodguy/cmd/core"
	"github.com/goodguy-project/goodguy/cmd/crawl"
	"github.com/goodguy-project/goodguy/cmd/mysql"
	"github.com/goodguy-project/goodguy/cmd/page"
)

var ExecMap = map[string]func(){
	"mysql.stop":          mysql.Stop,
	"mysql.backup":        mysql.Backup,
	"mysql.clean":         mysql.Clean,
	"mysql.deploy":        MysqlDeploy,
	"mysql.force.restart": mysql.ForceRestart,
	"core.restart":        core.Restart,
	"page.restart":        page.Restart,
	"crawl.restart":       crawl.Restart,
	"all":                 DeployAll,
}

func MysqlDeploy() {
	if len(os.Args) <= 2 {
		mysql.Deploy("")
	} else {
		mysql.Deploy(os.Args[2])
	}
}

func DeployAll() {
	if mysql.GetNameId() != "" {
		panic("goodguy-mysql container exists. run `mysql.backup` and `mysql.clean` first.")
	}
	wg := sync.WaitGroup{}
	wg.Add(2)
	go func() {
		crawl.Restart()
		wg.Done()
	}()
	go func() {
		page.Restart()
		wg.Done()
	}()
	mysql.Deploy("")
	time.Sleep(20 * time.Second) // wait for mysql
	core.Restart()
	wg.Wait()
	fmt.Println("deploy all done!")
}

func main() {
	if len(os.Args) <= 1 {
		output := "command with:\n"
		for k := range ExecMap {
			output += "  " + k + "\n"
		}
		fmt.Println(output)
		return
	}
	cmd := os.Args[1]
	if f, ok := ExecMap[cmd]; ok {
		f()
	} else {
		fmt.Printf("no command with '%s'\n", cmd)
	}
}
