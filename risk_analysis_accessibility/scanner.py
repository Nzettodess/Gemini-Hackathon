import ssl

ssl._create_default_https_context = ssl._create_unverified_context
# ----------------

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from axe_selenium_python import Axe
import json


def scan_accessibility(url):
    """
    使用 Selenium 和 Axe-core 扫描网页的无障碍问题
    """
    print(f"[*] Starting accessibility scan for: {url}")

    # 1. 自动下载并安装匹配版本的 chromedriver
    # 注意：这里的 verify=False 是为了配合上面的 SSL 忽略
    chromedriver_autoinstaller.install()

    # 2. 设置无头浏览器 (不在桌面显示窗口)
    options = Options()
    # 如果运行报错，可以尝试注释掉下面这一行 '--headless' 看看浏览器是否弹窗
    options.add_argument("--headless")

    # 解决部分沙盒权限问题
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        # 3. 访问目标网页
        driver.get(url)

        # 4. 注入 Axe-core 进行扫描
        axe = Axe(driver)
        axe.inject()
        # 运行检查
        results = axe.run()

        # 5. 提取违规项 (Violations)
        violations = results.get('violations', [])
        print(f"[*] Scan complete. Found {len(violations)} accessibility violations.")

        # 简单清理数据，只保留关键信息
        simplified_report = []
        for v in violations:
            item = {
                "impact": v.get('impact'),  # 严重程度
                "description": v.get('description'),  # 问题描述
                "help": v.get('help'),  # 修复建议
                "tags": v.get('tags')  # 涉及的WCAG标准
            }
            simplified_report.append(item)

        return simplified_report

    except Exception as e:
        print(f"[!] Error during scan: {e}")
        return []
    finally:
        # 确保浏览器关闭
        if 'driver' in locals():
            driver.quit()


# 测试代码
if __name__ == "__main__":
    target_url = "https://www.google.com"
    report = scan_accessibility(target_url)
    # 打印结果看看
    print(json.dumps(report, indent=2))
