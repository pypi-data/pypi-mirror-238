import testadr

from pages.adr_page import DemoPage


@testadr.story('测试demo')
class TestAdrDemo(testadr.TestCase):
    def start(self):
        self.page = DemoPage(self.driver)

    @testadr.title('进入设置页')
    def test_go_setting(self):
        self.page.adBtn.click_exists(timeout=5)
        self.page.myTab.click()
        self.page.settingBtn.click()
        self.assert_act('.me.MeSettingActivity')
        self.screenshot("设置页")


if __name__ == '__main__':
    testadr.main(
        devices=["UJK0220521066836"],
        pkg_name='com.qizhidao.clientapp'
    )


