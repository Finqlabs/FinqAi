from typing import final

from finq.browser.context import Context
from finq.browser.node_type import finqNode
from finq.browser.snapshot import BrowserSnapshot
from finq.pipe.preprocessing.a11y.tree import ProcessedA11yTree


@final
class ActionA11yPipe:

    @staticmethod
    def forward(snapshot: BrowserSnapshot) -> Context:
        processed_tree = ProcessedA11yTree.from_a11y_tree(snapshot.a11y_tree)
        return Context(
            snapshot=snapshot,
            node=finqNode.from_a11y_node(
                node=processed_tree.processed_tree,
                path=snapshot.metadata.url,
            ),
        )
