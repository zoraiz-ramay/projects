from graph import Graph


def print_banner(text: str, symbol: str = "="):
    print(symbol * len(text))
    print(text)
    print(symbol * len(text))

# ---- Main Script Starts Here ----
if __name__ == "__main__":

    print_banner("IntroCS: Graphs - Social Network Analysis applied to Mastodon data")

    # ---- Exercise 1.1: Implement Graph and User class, then visualize Mastodon_network ----
    print_banner("Exercise 1.1: Graph implementation", "-")

    # We provide you two datasets to try out your implementation. By default, it should use the followers, which we visualized
    # on the IntroCS Website (https://introcs.is.rw.fau.de/landing_page/pset8_mastodon_sna/)
    # If you want to use a bigger real life dataset, you can change the next line to "g=Graph()
    g = Graph()
    print("Parsing real-world data from Mastodon API...")
    g.parse_data('ressources/followers_example.json')

    print("Creating Mastodon_network visualization...")
    g.show()
    print("Network visualization created and stored as a PNG file.\n")


    # ---- Exercise 1.2: Check connectivity of graph ----
    print_banner("Exercise 1.2: Network Connectivity (DFS)", "-")

    subgraphs = g.get_subgraphs()
    status = "connected" if len(subgraphs) == 1 else "disconnected"
    # We expect the answer: "Our disconnected Mastodon_network consists of 2 disconnected subgraphs."
    print(f"Our {status} Mastodon_network consists of {len(subgraphs)} {status} {'subgraph' if len(subgraphs) == 1 else 'subgraphs'}.\n")



    # ---- Exercise 1.3: Find the shortest path connecting two users ----
    print_banner("Exercise 1.3: Shortest Path (BFS with path tracking)", "-")
    # We expect the anwer: "The shortest_path between Mark and Jack is ['Mark', 'Sundar', 'Jack']"
    user1, user2 = "Mark", "Jack"
    shortest_path = g.shortest_path(user1, user2)


    if shortest_path:
        print(f"The shortest_path between {user1} and {user2} is {shortest_path}.\n")
    else:
        print(f"There exists no connection between {user1} and {user2}.\n")

    # ---- Exercise 1.4: Find the most influential users ----
    print_banner("Exercise 1.4: Most Influential Users (Closeness)", "-")

    most_influential_users = g.most_influential()
    print("The most influential users in the mastodon_network are:")
    # We expect the answer: "Sundar, with an average shortest path length of 2.3 to all other users."
    for user, avg_length in most_influential_users:
        print(f"- {user}, with an average shortest path length of {avg_length} to all other users.")
    print()
    # Optionally: let self.most_influential() print out the average length of all average shortest path lengths.

    # ---- Exercise 1.5: Detect communities within the Mastodon_network ----
    print_banner("Exercise 1.5: Community Detection (Girvan Newman Algorithm)", "-")

    # Remove already existing clusters of single users
    remove = [i[0] for i in g.get_subgraphs() if len(i) == 1]
    for user in remove:
        g.remove_vertex(user)

    n = 2
    communities = g.girvan_newman_algorithm(clusters=n)
    print(f"For n = {n} clusters, the Girvan Newman algorithm detected the following communities:")
    # We expect the answer: Community 1 - ['Sundar', 'Adam', 'Elon', 'Marissa', 'Mark', 'Jack', 'Emanuel', 'Joe', 'Olaf', 'Rishi', 'Tim']
    #                       Community 2 - ['Brittany', 'Serge', 'Mary', 'Stephanie']
    for i, c in enumerate(communities, 1):
        print(f"\tCommunity {i} - {c}")

    print("Creating final visualization with identified communities...")
    g.show()
    print("Visualization updated and stored as a PNG file.\n")

    print_banner("End of Problem Set")