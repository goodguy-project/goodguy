package util

import (
	"path"
	"runtime"
	"sync"

	"github.com/spf13/viper"
)

var (
	once sync.Once
	vp   = viper.New()
)

func Viper() *viper.Viper {
	once.Do(func() {
		_, fileName, _, _ := runtime.Caller(0)
		vp.SetConfigName("config.yaml")
		vp.SetConfigType("yaml")
		configPath := path.Dir(path.Dir(fileName))
		vp.AddConfigPath(configPath)
		err := vp.ReadInConfig()
		if err != nil {
			panic(err)
		}
	})
	return vp
}
