# 🔍 Subenum — Automated Subdomain Enumeration Tool

**Subenum** is a Python-based automation tool that runs a curated set of subdomain enumeration tools in two optimized phases: **Fast** and **Slow**. It collects, deduplicates, and saves clean subdomain results in a single output file.

Whether you're a bug bounty hunter, red teamer, or security researcher, Subenum accelerates your recon phase by wrapping multiple tools into a single, streamlined workflow.

---

## ✨ Features

- ⚡ Fast & Slow tool execution phases
- 🧵 Multi-threaded execution
- ⏳ ETA estimation per phase
- 🧹 Automatic deduplication of results
- 📁 Organized output saving
- 💻 Works globally via symbolic link
- ✅ Minimal Python dependencies

---

## 🧰 Tools Used

| Tool         | Phase   |
|--------------|---------|
| assetfinder  | Fast    |
| subfinder    | Fast    |
| findomain    | Fast    |
| theHarvester | Fast    |
| amass        | Fast    |
| sublist3r    | Fast    |
| dnsrecon     | Slow    |
| dnsenum      | Slow    |
| fierce       | Slow    |
| gobuster     | Slow    |
| massdns      | Slow    |

---

## 🚀 Installation

### 🔹 Step 1: Clone the Repository


git clone https://github.com/akshigour12/Subdomain_Enum

cd Subdomain_Enum

chmod +x main.py

Step 2: Install Required Tools

sudo apt install assetfinder subfinder findomain amass theharvester dnsrecon dnsenum fierce gobuster massdns


Step 3 (Optional): Run from anywhere

sudo ln -s $(pwd)/main.py /usr/local/bin/subenum

Now you can run the tool globally using: subenum -d example.com -o results/example.txt

**Help Menu**
usage: subenum --help
optional arguments:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        Target domain
  -o OUTPUT, --output OUTPUT
                        Output file to save unique results


