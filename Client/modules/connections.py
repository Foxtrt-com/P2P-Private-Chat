# /modules/connections.py

class Connections:
    def __init__(self):
        self.peers = []
        self.current = 0

    def __get__(self, instance, owner):
        return self.peers

    def add(self, peer):
        if peer not in self.peers:
            self.peers.append(peer)
        return self.peers

    def sub(self, peer):
        if peer in self.peers:
            self.peers.remove(peer)
        return self.peers

    def __len__(self):
        return len(self.peers)

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < len(self.peers):
            return_val = self.peers[self.current]
            self.current += 1
            return return_val

        raise StopIteration

    def list_of_peers(self):
        return_val = []
        for peer in self.peers:
            return_val.append(peer)

        return return_val
