This folder contains the full SEO Master skill bundle (SKILL.md + reference .md files).
The API loads SKILL.md and appends the other markdown files in skill_loader.py.

After `git pull` on EC2, restart the service if you change these files:
  sudo systemctl restart hosted-skill-api

Optional: SKILL_PACKAGE_README.md is the human-facing description of the Cursor skill package.
