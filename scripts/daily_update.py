
import json
import os
import subprocess
from datetime import datetime, timezone

def get_repo_details(repo_name):
    """Fetches repository details from the GitHub API using the gh cli."""
    try:
        # Using gh api to get repo details
        command = [
            'gh', 'api',
            f'repos/{repo_name}',
            '--jq', '.name, .html_url, .description, .stargazers_count, .forks_count, .language, .created_at, .pushed_at'
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        # The output is tab-separated.
        name, url, desc, stars, forks, language, created_at, pushed_at = result.stdout.strip().split('\t')

        return {
            "name": repo_name,
            "url": url,
            "desc": desc if desc != "null" else "",
            "stars": int(stars),
            "forks": int(forks),
            "language": language if language != "null" else "N/A",
            "created_at": created_at,
            "pushed_at": pushed_at,
        }
    except subprocess.CalledProcessError as e:
        print(f"Error fetching details for {repo_name}: {e.stderr}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred for {repo_name}: {e}")
        return None

def main():
    """Main function to find new projects, update projects.json, and generate a report."""
    projects_file = '/home/admin/github-project-directory/data/projects.json'
    
    # --- 1. Load existing projects ---
    try:
        with open(projects_file, 'r', encoding='utf-8') as f:
            all_projects = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        all_projects = []

    existing_urls = {p['url'] for p in all_projects}

    # --- 2. Define candidate projects to investigate ---
    # Prioritizing official, active, high-growth projects in the AI agent space.
    candidate_repos = [
        "microsoft/UFO",          # New, high-growth, from Microsoft Research. UI-focused agent.
        "mindsdb/mindsdb",        # Established but very active, connects AI models to data. Agent-like capabilities.
        "NExT-GPT/NExT-GPT",      # Multimodal agent framework.
        "e2b-dev/e2b",            # Secure sandboxed environments for AI agents.
        "Superpower/Superpower-Desktop", # Local-first desktop AI agent.
        "all-in-aigc/agent-flan", # A new agent framework.
        "lavague-ai/lavague"      # Large Action Model for web automation.
    ]

    new_projects_to_add = []
    
    print("--- Fetching details for candidate projects ---")
    for repo_name in candidate_repos:
        repo_details = get_repo_details(repo_name)
        if repo_details and repo_details['url'] not in existing_urls:
            print(f"  + Found new project: {repo_name}")
            
            # --- 3. Manually add Chinese description and other metadata ---
            # This part requires manual intervention to ensure quality.
            desc_cn = ""
            icon = "".join([word[0] for word in repo_name.split("/")[1].split("-")[:2]]).upper()
            
            if repo_name == "microsoft/UFO":
                desc_cn = "微软研究院推出的新型 AI Agent，专为 Windows UI 操作而设计，能像人一样操作应用软件，完成复杂的跨应用任务。"
                icon = "UFO"
            elif repo_name == "mindsdb/mindsdb":
                desc_cn = "将 AI 模型连接到数据源的平台，使数据库具备预测能力，可像查询数据一样查询 AI 模型，实现智能数据处理和 Agent 功能。"
                icon = "MDB"
            elif repo_name == "NExT-GPT/NExT-GPT":
                desc_cn = "一个多模态大模型框架，能够接收和处理文本、图像、视频、音频等多种输入，并生成多种模态的输出，是构建通用多模态 Agent 的重要探索。"
                icon = "NG"
            elif repo_name == "e2b-dev/e2b":
                desc_cn = "为 AI Agent 提供安全的云端沙盒环境，让 Agent 可以在隔离的计算环境中执行代码、安装依赖、访问文件系统，解决了 Agent 的安全执行问题。"
                icon = "E2B"
            elif repo_name == "Superpower/Superpower-Desktop":
                desc_cn = "一款运行在桌面端的本地优先 AI 助手，可以访问计算机的上下文，自动化执行任务，并与本地应用集成。"
                icon = "SP"
            elif repo_name == "all-in-aigc/agent-flan":
                desc_cn = "一个旨在简化 AI Agent 开发的框架，提供模块化的组件和工具，帮助开发者快速构建、测试和部署 Agent 应用。"
                icon = "AF"
            elif repo_name == "lavague-ai/lavague":
                desc_cn = "一个为浏览器自动化设计的开源大型动作模型 (LAM)，能将自然语言指令转化为浏览器操作代码 (Selenium/Playwright)，实现端到端的网页自动化。"
                icon = "LV"


            # Create the new project entry
            new_project = {
                "name": repo_name,
                "category": "AI Agents",
                "url": repo_details['url'],
                "desc": repo_details['desc'],
                "tags": ["ai-agent", "automation", repo_details['language'].lower()] if repo_details['language'] else ["ai-agent", "automation"],
                "badge": "New Agent",
                "featured": True, # New projects are featured for visibility
                "category_cn": "AI 智能体",
                "icon": icon,
                "desc_cn": desc_cn,
                "stars": repo_details['stars'],
                "forks": repo_details['forks'],
                "language": repo_details['language'],
                "growth": {
                    "stars_per_day": round(repo_details['stars'] / ((datetime.now(timezone.utc) - datetime.fromisoformat(repo_details['created_at'].replace('Z', '+00:00'))).days + 1), 2),
                    "created_at": repo_details['created_at'],
                    "pushed_at": repo_details['pushed_at'],
                    "synced_at": datetime.now(timezone.utc).isoformat() + 'Z'
                }
            }
            new_projects_to_add.append(new_project)
            existing_urls.add(repo_details['url']) # Add to set to avoid duplicates within this run

    # --- 4. Add new projects to the list and save ---
    if new_projects_to_add:
        print(f"\n--- Adding {len(new_projects_to_add)} new projects to projects.json ---")
        # Prepend new projects to make them appear at the top
        updated_projects = new_projects_to_add + all_projects
        
        with open(projects_file, 'w', encoding='utf-8') as f:
            json.dump(updated_projects, f, indent=2, ensure_ascii=False)
        print("Successfully updated data/projects.json")
    else:
        print("\n--- No new projects found to add. ---")

if __name__ == "__main__":
    main()
