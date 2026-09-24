# Putting this project on GitHub

## 1. Create the repository
On github.com: **New repository** → name it `akshar-nursery-analytics` → Public → **Create repository**
(do not add a README; this project already has one).

## 2. Upload

**Option A: in the browser (no software needed)**
On the new repository page click **uploading an existing file**, drag in everything inside the
`akshar-nursery-analytics` folder (not the folder itself), and click **Commit changes**.

**Option B: with Git**
```bash
cd akshar-nursery-analytics
git init
git add .
git commit -m "Akshar Farm And Nursery: website and sales data analysis"
git branch -M main
git remote add origin https://github.com/hetachavda/akshar-nursery-analytics.git
git push -u origin main
```

## 3. Publish the website and dashboard (GitHub Pages)
Repository **Settings → Pages** → Source: **Deploy from a branch** → Branch: `main`, folder `/ (root)` → **Save**.
After a minute or two:
- Landing page: `https://hetachavda.github.io/akshar-nursery-analytics/`
- Website: `.../akshar-nursery-analytics/website/`
- Dashboard: `.../akshar-nursery-analytics/dashboard/`

## 4. Finishing touches
- Add your LinkedIn URL at the bottom of `README.md` (replace `YOUR-LINKEDIN`).

- Repository **About** (gear icon): add the Pages link as the website and topics such as
  `data-analysis`, `python`, `sql`, `pandas`, `small-business`, `portfolio`.
- Pin the repository on your GitHub profile.
