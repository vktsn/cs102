import igraph
import time
from api import get_friends
from igraph import Graph, plot
import config


def get_network(users_ids, as_edgelist=True) -> list:
    graph = []
    matrix = [[0 for i in range(len(users_ids))]
              for j in range(len(users_ids))]

    for user1 in range(len(users_ids)):
        response = get_friends(users_ids[user1])
        friends_list = response
        for user2 in range(user1 + 1, len(users_ids)):
            if users_ids[user2] in friends_list:
                if as_edgelist:
                    graph.append((user1, user2))
                else:
                    matrix[user1][user2] = 1
                    matrix[user2][user1] = 1
        time.sleep(0.4)
        print("loading...")

    if as_edgelist:
        return graph
    else:
        return matrix


def plot_graph(graph):
    friends = get_friends(124276053)
    # количество вершин
    vertices = [i for i in range(len(friends))]
    # ребра графа
    edges = graph
    # создание графа
    g = Graph(vertex_attrs={"label": vertices, "shape": "circle", "size": 10},
              edges=edges, directed=False)

    # стиль отображения графа
    n = len(vertices)
    visual_style = {
        # размер вершин
        "vertex_size": 20,
        # цвет граней
        "edge_color": "gray",
        "layout": g.layout_fruchterman_reingold(
            maxiter=1000,
            area=n ** 3,
            repulserad=n ** 3)
    }

    # удаляем петли и повторяющиеся ребра
    g.simplify(multiple=True, loops=True)

    # разделяем вершины на группы по взаимосвязям
    clusters = g.community_multilevel()
    print(clusters)

    # раскрашиваем разные группы вершин в разные цвета
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)

    # отрисовываем граф
    plot(g, **visual_style)


if __name__ == '__main__':
    user_id = int(config.VK_CONFIG['friend_id'])
    response = get_friends(user_id)
    graph = get_network(response, as_edgelist=True)
    plot_graph(graph)
