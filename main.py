#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Subdomain Enumerator - Fast and Slow Tool Queue with ETA
Author: Akshita Gour

Description:
    This script runs multiple subdomain enumeration tools in parallel, grouped
    into fast and slow phases. The results are deduplicated and saved into an
    output file for further analysis.

Usage:
    python3 main.py -d example.com -o output/example_subdomains.txt

Options:
    -d, --domain      Target domain to enumerate
    -o, --output      Output file path to save unique subdomains

Example:
    python3 main.py -d kali.org -o results/kali_subs.txt
"""

import os
import subprocess
import argparse
import concurrent.futures
import time
from queue import Queue
import shutil
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

TOOL_ESTIMATES = {
    "assetfinder": 5,
    "subfinder": 7,
    "findomain": 5,
    "theHarvester": 10,
    "amass": 15,
    "sublist3r": 10,
    "dnsrecon": 25,
    "dnsenum": 30,
    "fierce": 30,
    "gobuster": 35,
    "massdns": 40,
}

def run_tool(name, cmd, output_q):
    start = time.time()
    logging.info(f"Running: {name}")

    if shutil.which(cmd.split()[0]) is None:
        logging.warning(f"{name} not found. Skipping...")
        return

    try:
        result = subprocess.check_output(
            cmd, shell=True, stderr=subprocess.DEVNULL, timeout=180
        ).decode("utf-8", errors="ignore")
        output_q.put((name, result))
        logging.info(f"Finished: {name} in {int(time.time() - start)}s")
    except subprocess.TimeoutExpired:
        logging.warning(f"{name} timed out.")
    except Exception as e:
        logging.error(f"{name} failed: {str(e)}")

def estimate_total_time(tool_list):
    return sum(TOOL_ESTIMATES.get(tool[0], 10) for tool in tool_list)

def main():
    parser = argparse.ArgumentParser(
        description="Run subdomain tools in fast-then-slow queue with ETA."
    )
    parser.add_argument("-d", "--domain", required=True, help="Target domain")
    parser.add_argument("-o", "--output", required=True, help="Output file to save unique results")
    args = parser.parse_args()

    domain = args.domain
    output_file = args.output
    output_queue = Queue()

    all_tools = [
        ("assetfinder", f"assetfinder --subs-only {domain}"),
        ("subfinder", f"subfinder -d {domain}"),
        ("findomain", f"findomain -t {domain} -u -"),
        ("theHarvester", f"theHarvester -d {domain} -b all"),
        ("amass", f"amass enum -passive -d {domain}"),
        ("sublist3r", f"python3 /usr/local/bin/sublist3r -d {domain}"),
        ("dnsrecon", f"dnsrecon -d {domain}"),
        ("dnsenum", f"dnsenum {domain}"),
        ("fierce", f"fierce --domain {domain}"),
        ("gobuster", f"gobuster dns -d {domain} -w /usr/share/wordlists/dirb/common.txt -q"),
        ("massdns", f"massdns -r /etc/resolv.conf -t A -o S -w massdns.txt {domain}")
    ]

    fast_tools = ["assetfinder", "subfinder", "findomain", "theHarvester", "amass", "sublist3r"]
    fast_phase = [t for t in all_tools if t[0] in fast_tools]
    slow_phase = [t for t in all_tools if t[0] not in fast_tools]

    total_fast_time = estimate_total_time(fast_phase)
    total_slow_time = estimate_total_time(slow_phase)

    logging.info(f"\n⏳ Phase 1: Fast tools (~{total_fast_time}s)")
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        fast_futures = [executor.submit(run_tool, name, cmd, output_queue) for name, cmd in fast_phase]
        concurrent.futures.wait(fast_futures)

    logging.info(f"\n⏳ Phase 2: Slow tools (~{total_slow_time}s)")
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        slow_futures = [executor.submit(run_tool, name, cmd, output_queue) for name, cmd in slow_phase]
        concurrent.futures.wait(slow_futures)

    all_results = set()
    while not output_queue.empty():
        name, output = output_queue.get()
        for line in output.splitlines():
            line = line.strip()
            if line and args.domain in line:
                all_results.add(line)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w") as f:
        for subdomain in sorted(all_results):
            f.write(subdomain + "\n")

    logging.info(f"\n✅ Unique subdomains saved to {output_file} (Total: {len(all_results)})")

if __name__ == "__main__":
    main()
