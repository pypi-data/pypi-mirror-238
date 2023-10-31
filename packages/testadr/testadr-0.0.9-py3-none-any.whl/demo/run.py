import testadr


if __name__ == '__main__':
    # 执行多个用例文件，主程序入口

    testadr.main(
        case_path='tests',
        devices=["UJK0220521066836"],
        pkg_name='com.qizhidao.clientapp',
    )



