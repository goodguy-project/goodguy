package page

import (
	"github.com/goodguy-project/goodguy/cmd/util"
)

func CloneCode() {
	_ = util.RunCmd("git clone https://github.com/goodguy-project/goodguy-page.git")
}

func Restart() {
	CloneCode()
	_ = util.RunCmd("cd goodguy-page && make docker.clean && make docker.build")
	_ = util.RunCmd("docker network create goodguy-net")
	_ = util.RunCmd("docker run -p 80:80 -dit --name=\"goodguy-page\" --restart=always --network goodguy-net --network-alias goodguy-page goodguy-page")
}
