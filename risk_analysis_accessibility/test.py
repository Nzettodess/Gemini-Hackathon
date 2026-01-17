import unittest

from main import AccessibilityAgent


class TestAccessibilityAgent(unittest.TestCase):

    def test_agent_initialization(self):
        """测试 Agent 能否正常初始化"""
        agent = AccessibilityAgent()
        self.assertIsNotNone(agent)

    def test_audit_workflow(self):
        """测试能不能跑通一个真实的网站（比如 Example.com）"""
        agent = AccessibilityAgent()
        # example.com 很简单，跑得快
        report, path = agent.run_audit("https://example.com")

        # 断言：必须生成了报告内容
        self.assertIsNotNone(report)
        # 断言：必须包含了基本的法律关键词
        self.assertIn("Fundamental Rights", report)
        print(f"\nTest passed! Report generated at: {path}")


if __name__ == '__main__':
    unittest.main()
