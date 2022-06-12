package mysql

import (
	"strings"

	"github.com/goodguy-project/goodguy/cmd/util"
)

const (
	ContainerName        = "goodguy-mysql"
	BackupImageName      = "goodguy-mysql-bak"
	BackupFileName       = "goodguy-mysql-bak.tar"
	SourceMysqlImageName = "mysql:8.0-oracle"
)

func GetNameId() string {
	s := util.RunCmd(`docker ps -a -q --filter="name=%s"`, ContainerName)
	return strings.Trim(s, "\r\n ")
}

func Stop() {
	id := GetNameId()
	_ = util.RunCmd("docker stop %s", id)
}

func Backup() {
	id := GetNameId()
	_ = util.RunCmd("docker commit %s %s", id, BackupImageName)
	_ = util.RunCmd("docker save -o %s %s", BackupFileName, BackupImageName)
}

func Clean() {
	Stop()
	id := GetNameId()
	_ = util.RunCmd("docker rm %s", id)
}

func Deploy(tar string) {
	_ = util.RunCmd("docker network create goodguy-net")
	if tar != "" {
		_ = util.RunCmd("docker load -i %s", tar)
		_ = util.RunCmd(`docker run -dit --restart=always --name="goodguy-mysql" --network goodguy-net --network-alias goodguy-mysql -p 127.0.0.1:9854:3306 -e MYSQL_ROOT_PASSWORD=goodguy -e MYSQL_DATABASE=goodguy_core %s`, BackupImageName)
	} else {
		_ = util.RunCmd(`docker run -dit --restart=always --name="goodguy-mysql" --pull=always --network goodguy-net --network-alias goodguy-mysql -p 127.0.0.1:9854:3306 -e MYSQL_ROOT_PASSWORD=goodguy -e MYSQL_DATABASE=goodguy_core %s`, SourceMysqlImageName)
	}
}

// ForceRestart 强制清除所有数据 并重新部署
func ForceRestart() {
	Clean()
	Deploy("")
}
