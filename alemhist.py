# This script is under GNU General Public licence v3.
# See the root of the project or https://www.gnu.org/licenses/gpl-3.0.en.html

from __future__ import annotations
from io import TextIOBase
from typing import Iterable, Mapping
from colorama import Fore, Style
import sys

use_colors = False

def main(argv: list[str]):
	argv.pop(0)

	global use_colors
	if "--color" in argv:
		use_colors = True
		argv.remove("--color")

	stream = sys.stdin
	if len(argv) >= 1:
		stream = open(argv[0], "r")

	graph, order = parse_graph(stream)
	visu = text_graph_visu(graph, order)
	print(visu)


class Node:
	def __init__(self, preds: list[str], succs: list[str] = [], label = ""):
		self.preds = preds
		self.succs = succs
		self.label = label


def build_label(id_: str, tags: Iterable[str], label: str):
	if use_colors:
		id_ = Fore.YELLOW + id_ + Style.RESET_ALL
		tags = [Fore.GREEN+Style.BRIGHT + tag + Style.RESET_ALL for tag in tags]
		if label == "empty message":
			label = Fore.LIGHTBLACK_EX + label + Style.RESET_ALL
	return " ".join([id_, *tags, label])

def parse_graph(readable_text_stream: TextIOBase) -> tuple[dict[str, Node], list[str]]:
	""" Get an alembic history from a stream and parse it to extract the DAG and
	the child -> parent order """
	order = []
	graph = {}

	with readable_text_stream as stream:
		for line in stream.readlines():
			line = line.rstrip("\n")
			arrowsplit = line.split(" -> ")
			if len(arrowsplit) < 2:
				# It's not a graph line, it's a continuation of the previous label
				if order:
					graph[order[-1]].label += " " + line
				continue
			preds = arrowsplit.pop(0).split(", ")
			commasplit = arrowsplit.pop(0).split(", ")
			id_and_tags = commasplit.pop(0).split(" ")
			id_ = id_and_tags.pop(0)
			tags = filter(lambda tag: tag not in ["(branchpoint)", "(mergepoint)"], id_and_tags)
			label = build_label(id_, tags, ", ".join(commasplit) + "".join(" -> " + s for s in arrowsplit))
			preds = [p for p in preds if p != "<base>"]
			graph[id_] = Node(preds, [], label)
			order.append(id_)

	# Compute successors
	for node_id in order:
		node = graph[node_id]
		for pred in node.preds:
			if pred in graph and node_id not in graph[pred].succs:
				graph[pred].succs.append(node_id)

	return graph, order


def color_by_column(s: str, column: int):
	if not use_colors:
		return s
	COLORS = [Fore.GREEN, Fore.LIGHTBLUE_EX, Fore.RED, Fore.LIGHTCYAN_EX, Fore.MAGENTA,
		Fore.LIGHTYELLOW_EX, Fore.BLUE, Fore.LIGHTRED_EX, Fore.CYAN, Fore.LIGHTMAGENTA_EX]
	color = COLORS[column % len(COLORS)]
	return color + s + Style.RESET_ALL

def text_graph_visu(graph: Mapping[str, Node], order: list[str]):
	""" Vizalualize the given DAG into a text-based representation """
	lines: list[str] = []
	node_column: dict[str, int] = {}
	remaining: dict[int, int] = {}

	def first_available_column(preds: list[str]) -> int:
		# Search an available predecessor column (with no other remaining successor)
		preds = sorted(preds, key=lambda pred: node_column[pred])
		for pred in preds:
			if remaining[node_column[pred]] == 0:
				return node_column[pred]

		# No free predecessor column was found -> return the first empty column
		nb_col = max(remaining.keys()) + 1 if remaining else 0
		for col in range(nb_col):
			if col not in remaining:
				return col
		return nb_col

	for node_id in reversed(order):
		preds = graph[node_id].preds

		for pred in preds:
			remaining[node_column[pred]] -= 1

		# Choose the column for the current node
		current_column = first_available_column(preds)
		node_column[node_id] = current_column

		first_col =	min([current_column] + [node_column[p] + 1 for p in preds])
		last_col = max([current_column] + [node_column[p] - 1 for p in preds])
		nb_col = max(remaining.keys()) + 2 if remaining else 1

		quad_line = [[" "] * 4 for _ in range(nb_col)] # top-right, top-left, bottom-right, bottom-left
		for col in range(first_col + 1, current_column + 1):
			quad_line[col][0] = quad_line[col][1] = color_by_column("_", first_col - 1)
		for col in range(current_column + 1, last_col + 1):
			quad_line[col][0] = quad_line[col][1] = color_by_column("_", last_col + 1)
		for col in range(nb_col):
			if col in remaining and remaining[col] > 0:
				quad_line[col][0] = quad_line[col][2] = color_by_column("|", col)
		for pred in preds:
			if node_column[pred] == current_column:
				quad_line[current_column][2] = color_by_column("|", current_column)
			elif node_column[pred] < current_column:
				quad_line[node_column[pred] + 1][3] = color_by_column("/", node_column[pred])
			elif node_column[pred] > current_column:
				quad_line[node_column[pred]][3] = color_by_column("\\", node_column[pred])
		quad_line[current_column][0] = "*"

		# Insert current line and node's label in lines list
		top_line = (quad_line[i][1] + quad_line[i][0] for i in range(nb_col))
		top_line = "".join(top_line).rstrip()
		bot_line = (quad_line[i][3] + quad_line[i][2] for i in range(nb_col))
		bot_line = "".join(bot_line).rstrip()
		top_line += " " + graph[node_id].label
		if all(c[3] == " " for c in quad_line):
			# If bot_line only contains vertical bars and spaces, skip it
			lines.append(top_line)
		else:
			lines += [bot_line, top_line]

		# Update remainings for next row
		for pred in preds:
			if remaining[node_column[pred]] == 0:
				del remaining[node_column[pred]]
		if len(graph[node_id].succs):
			remaining[current_column] = len(graph[node_id].succs)

	# Reverse lines because we want the most recent migration on top
	return "\n".join(reversed(lines))


if __name__ == '__main__':
	main(sys.argv)
