package crawl

import (
	"os"
	"path"
	"sync"

	"github.com/spf13/viper"

	"github.com/goodguy-project/goodguy/cmd/util"
)

var (
	once sync.Once
	vp   = viper.New()
)

func Viper() *viper.Viper {
	once.Do(func() {
		var err error
		vp.SetConfigName("config.yml")
		vp.SetConfigType("yaml")
		wd, err := os.Getwd()
		if err != nil {
			panic(err)
		}
		configPath := path.Join(wd, "goodguy-crawl")
		vp.AddConfigPath(configPath)
		err = vp.ReadInConfig()
		if err != nil {
			panic(err)
		}
	})
	return vp
}

func CloneCode() {
	_ = util.RunCmd("git clone https://github.com/goodguy-project/goodguy-crawl.git")
}

func Restart() {
	CloneCode()
	Viper().Set("vjudge.username", util.Viper().Get("vjudge.username"))
	Viper().Set("vjudge.password", util.Viper().Get("vjudge.password"))
	err := Viper().WriteConfig()
	if err != nil {
		panic(err)
	}
	_ = util.RunCmd("cd goodguy-crawl && make restart")
}
