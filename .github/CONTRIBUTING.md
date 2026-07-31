# Contributing · 参与贡献

Thank you for improving Industrial Design Portfolio Skill. Contributions should preserve its evidence-first behavior and remain useful across supported Agent runtimes.

感谢你参与改进工业设计作品集 Skill。所有贡献都应保持“证据优先”的原则，并继续兼容项目支持的 Agent 运行环境。

## Before opening a pull request · 提交 PR 前

1. Create a focused branch from the latest `main`.
2. Keep `SKILL.md` as the canonical instruction source; run `python scripts/sync_adapters.py` after changing it.
3. Do not present generated imagery as research, prototypes, CAD, test results, or engineering evidence.
4. Do not add Showcase files, eval fixtures, or development dependencies to the installer runtime whitelist.
5. Run the validation commands below.

1. 从最新 `main` 创建单一目标的功能分支。
2. 将 `SKILL.md` 保持为规范源；修改后运行 `python scripts/sync_adapters.py`。
3. 不得把生成图描述成调研、实体原型、CAD、测试结果或工程证据。
4. 不要把 Showcase、eval fixtures 或开发依赖加入安装器运行时白名单。
5. 运行以下校验。

```bash
python scripts/sync_adapters.py --check
python scripts/validate_layout_library.py
python scripts/validate_manifest.py showcase/modular-desk-lamp/portfolio_manifest.json
python scripts/validate_portfolio.py showcase/modular-desk-lamp/index.html
python scripts/run_evals.py --all
python -m pip install --requirement requirements-test.txt
python -m unittest discover -s tests -p "test_*.py" -v
npm ci
npx playwright install chromium
npm run test:browser
```

Keep pull requests small, explain user impact, disclose AI-assisted assets, and include screenshots when visual output changes.

请保持 PR 范围清晰，说明用户影响，披露 AI 辅助素材，并在视觉输出变化时提供截图。
