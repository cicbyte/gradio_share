package main

import (
	"fmt"
	"goshare.com/m/tunnel"
	"goshare.com/m/utils"
	"log"
	"os"
	"path/filepath"
	"time"

	"github.com/spf13/cobra"
)

var (
	port    int
	address string
	binPath string
)

func main() {
	rootCmd := &cobra.Command{
		Use:   "gradio_share",
		Short: "将本地端口通过 Gradio 隧道暴露到公网",
		Long: `gradio_share 是一个本地端口隧道工具，通过 Gradio 的免费 frp 隧道服务
将本地服务暴露到公网，生成一个临时的公网访问 URL（有效期 72 小时）。`,
		Run: run,
	}

	rootCmd.Flags().IntVarP(&port, "port", "p", 8085, "要转发的本地端口")
	rootCmd.Flags().StringVarP(&address, "address", "a", "https://api.gradio.app/v2/tunnel-request", "分享服务器地址")
	rootCmd.Flags().StringVarP(&binPath, "binPath", "b", "", "frpc程序路径,默认查找可执行文件同级的bin目录")

	if err := rootCmd.Execute(); err != nil {
		os.Exit(1)
	}
}

func run(cmd *cobra.Command, args []string) {
	// 确定 frpc 二进制路径
	if binPath == "" {
		fileName := utils.GuessFrpcBinaryName()
		binPath = fmt.Sprintf("bin/%s", fileName)
	}

	// 校验 frpc 二进制文件是否存在
	if _, err := os.Stat(binPath); os.IsNotExist(err) {
		log.Fatalf("frpc 二进制文件路径不存在: %s\n", binPath)
	}

	// 设置为绝对路径
	binPath, _ = filepath.Abs(binPath)
	log.Printf("frpc程序路径:%s", binPath)
	log.Printf("分享服务器地址:%s\n", address)

	secretToken, err := utils.GenerateSecureToken(32)
	if err != nil {
		log.Fatalf("无法生成安全令牌: %v\n", err)
	}
	log.Printf("安全令牌: %s\n", secretToken)

	remoteHost, remotePort, _ := utils.GetServerInfo(address)

	log.Printf("转发的端口:%d\n", port)

	t := &tunnel.Tunnel{
		FrpcPath:   binPath,
		RemoteHost: remoteHost,
		RemotePort: remotePort,
		LocalHost:  "127.0.0.1",
		LocalPort:  port,
		ShareToken: secretToken,
	}

	fmt.Printf(t.String())
	url, err := t.Start()
	log.Printf("访问地址：%s\n", url)
	log.Println("连接有效期:72小时")
	// 等待72小时
	time.Sleep(72 * time.Hour)
}
