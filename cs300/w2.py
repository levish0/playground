def count_scc(vertex_cnt, edges):
    # 그래프랑 역그래프
    graph = [[] for _ in range(vertex_cnt+1)]
    inverse_graph = [[] for _ in range(vertex_cnt+1)]

    for u, v in edges:
        graph[u].append(v)
        inverse_graph[v].append(u)

    visited = set()
    stack = []

    # dfs로 연결된 것들을 돌아서 다 visited에 넣음
    def dfs(node):
        visited.add(node)
        for v in graph[node]:
            if v not in visited:
                dfs(v)
        stack.append(node)
    # 역
    def inv_dfs(node):
        visited.add(node)
        for v in inverse_graph[node]:
            if v not in visited:
                inv_dfs(v)

    # 아직 안 들른 노드는 scc가 아니므로 다시 dfs
    for i in range(1, vertex_cnt+1):
        if i not in visited:
            dfs(i)

    visited.clear()
    scc_count = 0

    while stack:
        node = stack.pop()
        if node not in visited:
            inv_dfs(node)
            scc_count+=1

    return scc_count