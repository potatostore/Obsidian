#!/usr/bin/env python3
import os
import json
import argparse
from organizer import VaultOrganizer

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>🔮 Obsidian Vault Organic Knowledge Graph</title>
    <!-- Tailwind CSS for utility styles (only for container positioning) -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Google Fonts Inter -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <!-- D3.js -->
    <script src="https://cdn.d3js.org/d3.v7.min.js"></script>
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background: radial-gradient(circle at center, #0f172a 0%, #020617 100%);
            color: #f8fafc;
            overflow: hidden;
            margin: 0;
            height: 100vh;
        }
        .glass-panel {
            background: rgba(15, 23, 42, 0.65);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }
        .node {
            cursor: pointer;
            transition: stroke 0.25s, filter 0.25s;
        }
        .node:hover {
            filter: drop-shadow(0 0 8px var(--glow-color));
        }
        .link {
            stroke-opacity: 0.15;
            stroke-width: 1.5px;
            transition: stroke-opacity 0.25s, stroke-width 0.25s;
        }
        .link.highlighted {
            stroke-opacity: 0.7;
            stroke-width: 2.5px;
        }
        .node-label {
            font-size: 11px;
            font-weight: 500;
            fill: #e2e8f0;
            pointer-events: none;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.9);
            transition: fill 0.2s, font-size 0.2s;
        }
        .node-label.active {
            font-size: 13px;
            font-weight: 700;
            fill: #ffffff;
        }
    </style>
</head>
<body class="relative">

    <!-- Header Panel -->
    <div class="absolute top-6 left-6 z-10 p-5 rounded-2xl glass-panel w-80 max-w-full">
        <h1 class="text-xl font-bold bg-gradient-to-r from-teal-400 via-indigo-400 to-purple-400 bg-clip-text text-transparent flex items-center gap-2">
            🔮 Obsidian Organic Graph
        </h1>
        <p class="text-xs text-slate-400 mt-1 mb-4">지식 그래프 관계 및 연결 구조 분석</p>
        
        <!-- Search bar -->
        <div class="mb-4">
            <label class="text-[10px] font-semibold tracking-wider text-slate-500 uppercase">노트 검색</label>
            <input type="text" id="search-input" placeholder="노트 제목 입력..." 
                   class="w-full bg-slate-950/80 border border-slate-800 rounded-lg py-2 px-3 text-xs text-slate-200 focus:outline-none focus:border-indigo-500 mt-1 placeholder-slate-600 transition-all">
        </div>

        <!-- Details Box -->
        <div id="details-box" class="p-3 bg-slate-950/40 border border-slate-900 rounded-lg text-xs">
            <span class="text-slate-500">노트를 클릭하면 상세 정보가 표시됩니다.</span>
        </div>
        
        <div class="mt-4 flex gap-4 text-[10px] text-slate-400 border-t border-slate-800/60 pt-3">
            <div>노트 수: <span id="stat-nodes" class="font-bold text-teal-400">-</span></div>
            <div>연결 수: <span id="stat-links" class="font-bold text-indigo-400">-</span></div>
            <div>독립 노트: <span id="stat-orphans" class="font-bold text-rose-400">-</span></div>
        </div>
    </div>

    <!-- Filter Panel (Top Right) -->
    <div class="absolute top-6 right-6 z-10 p-4 rounded-xl glass-panel text-xs flex flex-col gap-2">
        <span class="font-semibold text-slate-300">태그 필터</span>
        <div id="tag-legend" class="flex flex-col gap-1.5 max-h-48 overflow-y-auto pr-2 mt-1">
            <!-- Dynamic tags list -->
        </div>
    </div>

    <!-- SVG Canvas -->
    <svg id="graph-svg" class="w-full h-full"></svg>

    <script>
        // Inject compiled graph JSON
        const graphData = %GRAPH_JSON%;

        // Stats setup
        document.getElementById('stat-nodes').textContent = graphData.nodes.length;
        document.getElementById('stat-links').textContent = graphData.links.length;
        
        // Count orphans
        const connectedNodes = new Set();
        graphData.links.forEach(l => {
            connectedNodes.add(l.source);
            connectedNodes.add(l.target);
        });
        const orphanCount = graphData.nodes.filter(n => !connectedNodes.has(n.id)).length;
        document.getElementById('stat-orphans').textContent = orphanCount;

        // Visual Colors Config (Harmony HSL Palette)
        const colors = {
            "seed": "#f59e0b",       # Golden Amber
            "growing": "#10b981",    # Emerald
            "evergreen": "#3b82f6",  # Indigo Blue
            "default": "#a855f7",    # Purple
        };
        
        // Group nodes by tags
        const allTags = new Set();
        graphData.nodes.forEach(node => {
            if (node.tags && node.tags.length > 0) {
                node.tags.forEach(t => allTags.add(t));
            }
        });
        
        // Populate Tag Filter list
        const legendContainer = document.getElementById('tag-legend');
        Array.from(allTags).sort().forEach(tag => {
            const row = document.createElement('div');
            row.className = 'flex items-center gap-2 cursor-pointer hover:bg-slate-800/40 p-1 rounded transition-all';
            
            let color = colors.default;
            if (colors[tag]) color = colors[tag];
            
            row.innerHTML = `
                <span class="w-2.5 h-2.5 rounded-full" style="background-color: ${color}; box-shadow: 0 0 6px ${color}"></span>
                <span class="text-[11px] text-slate-300">#${tag}</span>
            `;
            row.onclick = () => highlightTag(tag);
            legendContainer.appendChild(row);
        });

        // Initialize SVG
        const svg = d3.select("#graph-svg");
        const width = window.innerWidth;
        const height = window.innerHeight;
        
        // Zoom functionality
        const zoomG = svg.append("g");
        const zoom = d3.zoom()
            .scaleExtent([0.1, 8])
            .on("zoom", (event) => {
                zoomG.attr("transform", event.transform);
            });
        svg.call(zoom);

        // Simulation setup
        const simulation = d3.forceSimulation(graphData.nodes)
            .force("link", d3.forceLink(graphData.links).id(d => d.id).distance(80))
            .force("charge", d3.forceManyBody().strength(-150))
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force("collision", d3.forceCollide().radius(25));

        // Draw Links
        const link = zoomG.append("g")
            .attr("class", "links-layer")
            .selectAll("line")
            .data(graphData.links)
            .join("line")
            .attr("class", "link")
            .attr("stroke", "#475569");

        // Draw Nodes
        const node = zoomG.append("g")
            .attr("class", "nodes-layer")
            .selectAll("g")
            .data(graphData.nodes)
            .join("g")
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));

        // Render circles with neon glow based on status or tags
        node.append("circle")
            .attr("r", d => d.linksCount ? Math.min(18, 5 + d.linksCount * 1.5) : 6)
            .attr("fill", d => {
                const primaryTag = d.tags && d.tags[0];
                return colors[primaryTag] || colors.default;
            })
            .style("--glow-color", d => {
                const primaryTag = d.tags && d.tags[0];
                return colors[primaryTag] || colors.default;
            })
            .attr("class", "node")
            .attr("stroke", "#1e293b")
            .attr("stroke-width", 1.5);

        // Labels
        const label = node.append("text")
            .attr("dy", 18)
            .attr("text-anchor", "middle")
            .attr("class", "node-label")
            .text(d => d.title);

        // Update Sim
        simulation.on("tick", () => {
            link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);

            node
                .attr("transform", d => `translate(${d.x}, ${d.y})`);
        });

        // Interactive highlight events
        node.on("click", (event, d) => {
            event.stopPropagation();
            showDetails(d);
            highlightNodeConnections(d);
        });

        svg.on("click", () => {
            resetHighlight();
        });

        // Search Bar Event Listener
        document.getElementById('search-input').addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase().trim();
            if (!query) {
                resetHighlight();
                return;
            }
            
            node.style("opacity", d => d.title.toLowerCase().includes(query) ? 1.0 : 0.15);
            link.style("stroke-opacity", 0.05);
            label.style("fill", d => d.title.toLowerCase().includes(query) ? "#ffffff" : "#475569");
        });

        function showDetails(d) {
            const box = document.getElementById('details-box');
            const tagsMarkup = d.tags && d.tags.length > 0 
                ? d.tags.map(t => `<span class="bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 px-2 py-0.5 rounded text-[10px]">#${t}</span>`).join(' ')
                : '<span class="text-slate-500">태그 없음</span>';
                
            box.innerHTML = `
                <div class="flex flex-col gap-2">
                    <div class="font-bold text-slate-100 text-sm">📄 ${d.title}</div>
                    <div class="text-[10px] text-slate-500">경로: ${d.path}</div>
                    <div class="flex flex-wrap gap-1 mt-1">${tagsMarkup}</div>
                    <div class="border-t border-slate-800/80 pt-2 mt-1 flex justify-between text-[10px] text-slate-400">
                        <span>인바운드(참조됨): <b>${d.backlinksCount || 0}</b></span>
                        <span>아웃바운드(참조함): <b>${d.linksCount || 0}</b></span>
                    </div>
                </div>
            `;
        }

        let highlightedNodeId = null;

        function highlightNodeConnections(selectedNode) {
            highlightedNodeId = selectedNode.id;
            
            // Find neighbors
            const neighbors = new Set([selectedNode.id]);
            graphData.links.forEach(l => {
                if (l.source.id === selectedNode.id) neighbors.add(l.target.id);
                if (l.target.id === selectedNode.id) neighbors.add(l.source.id);
            });

            // Dim everything except neighbors
            node.style("opacity", d => neighbors.has(d.id) ? 1.0 : 0.15);
            label.style("fill", d => neighbors.has(d.id) ? "#ffffff" : "#475569");
            
            // Highlight matching links
            link
                .classed("highlighted", l => l.source.id === selectedNode.id || l.target.id === selectedNode.id)
                .style("stroke-opacity", l => l.source.id === selectedNode.id || l.target.id === selectedNode.id ? 0.8 : 0.05)
                .style("stroke", l => l.source.id === selectedNode.id || l.target.id === selectedNode.id ? "#818cf8" : "#475569");
        }

        function highlightTag(tag) {
            node.style("opacity", d => d.tags && d.tags.includes(tag) ? 1.0 : 0.15);
            label.style("fill", d => d.tags && d.tags.includes(tag) ? "#ffffff" : "#475569");
            link.style("stroke-opacity", 0.05);
        }

        function resetHighlight() {
            highlightedNodeId = null;
            node.style("opacity", 1.0);
            label.style("fill", "#e2e8f0");
            link
                .classed("highlighted", false)
                .style("stroke-opacity", 0.15)
                .style("stroke", "#475569");
                
            document.getElementById('search-input').value = "";
        }

        // Dragging Event Handlers
        def dragstarted(event, d) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }

        function dragged(event, d) {
            d.fx = event.x;
            d.fy = event.y;
        }

        function dragended(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }
    </script>
</body>
</html>
"""

def generate_graph_data(organizer):
    """Formats nodes and links into standard graph.json structure."""
    nodes = []
    links = []
    
    # Pre-calculate backlinks
    backlinks = {title: 0 for title in organizer.notes}
    for title, note in organizer.notes.items():
        for target in note.links:
            if target in backlinks:
                backlinks[target] += 1

    for title, note in organizer.notes.items():
        nodes.append({
            "id": title,
            "title": title,
            "path": note.relpath,
            "tags": sorted(list(note.tags)),
            "linksCount": len(note.links),
            "backlinksCount": backlinks[title]
        })
        
        for target in note.links:
            # Only draw link if the target note exists in the vault
            if target in organizer.notes:
                links.append({
                    "source": title,
                    "target": target,
                    "value": 1
                })
                
    return {"nodes": nodes, "links": links}

def main():
    parser = argparse.ArgumentParser(description="Obsidian Graph Data Exporter & Visualizer")
    parser.add_argument("--vault", type=str, default="..", help="Path to your Obsidian Vault (defaults to parent directory)")
    
    args = parser.parse_args()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    vault_path = args.vault
    if vault_path == "..":
        vault_path = os.path.dirname(script_dir)
        
    organizer = VaultOrganizer(vault_path)
    organizer.scan_vault()
    
    graph_data = generate_graph_data(organizer)
    
    # 1. Export graph.json (perfect for Graphify)
    json_path = os.path.join(script_dir, "graph.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, ensure_ascii=False, indent=2)
    print(f"✔ Exported structured graph representation to: `.obsidian-agent/graph.json`")
    
    # 2. Export HTML Visualization
    html_path = os.path.join(script_dir, "preview.html")
    compiled_html = HTML_TEMPLATE.replace("%GRAPH_JSON%", json.dumps(graph_data, ensure_ascii=False))
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(compiled_html)
    print(f"✔ Generated interactive local visualization at: `.obsidian-agent/preview.html`")
    print(f"  💡 Open this file in your web browser to explore your gorgeous knowledge graph!")

if __name__ == "__main__":
    main()
