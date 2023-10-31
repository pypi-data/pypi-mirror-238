from auto_phylo.pipeliner.component.AutoPhyloPipeliner import AutoPhyloPipeliner


def launch():
    designer = AutoPhyloPipeliner()
    designer.minsize(width=900, height=600)
    designer.mainloop()


if __name__ == "__main__":
    launch()
