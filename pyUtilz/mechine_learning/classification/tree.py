from typing import Iterable
from sklearn import tree


def decision_tree_to_graph(clf: tree.DecisionTreeClassifier, feature_names: Iterable[str], class_names: Iterable[str],
                           graph_path: str, graphviz_path: str = None):
    if graphviz_path is not None:
        import os
        os.environ["PATH"] += os.pathsep + graphviz_path
    import pydotplus
    class_names = map(lambda n: str(n), class_names)
    dot_data = tree.export_graphviz(clf, feature_names=feature_names, class_names=sorted(class_names), filled=True,
                                    out_file=None)

    graph = pydotplus.graph_from_dot_data(dot_data)
    graph.write_png(graph_path)
