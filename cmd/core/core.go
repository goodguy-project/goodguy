package core

import "github.com/goodguy-project/goodguy/cmd/util"

func CloneCode() {
	_ = util.RunCmd("git clone https://github.com/goodguy-project/goodguy-core.git")
}

func Restart() {
	CloneCode()
	_ = util.RunCmd("cd goodguy-core && make restart")
}
