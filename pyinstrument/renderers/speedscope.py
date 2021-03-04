from pyinstrument.renderers.base import Renderer
from pyinstrument import processors


class SpeedscopeRenderer(Renderer):

    def render_frame(self, frame):
        this = f'{frame.function}'
        if not frame.children:
            return [f'{this} {int(frame.time() * 1e6)}']
        paths = []
        for child in frame.children:
            if child is None:
                continue
            paths.extend([f'{this};{p}' for p in self.render_frame(child)])
        return paths

    def render(self, session):
        frame = self.preprocess(session.root_frame())
        s = '\n'.join(self.render_frame(frame))
        return s

    def default_processors(self):
        return [
            processors.remove_importlib,
            processors.merge_consecutive_self_time,
            processors.aggregate_repeated_calls,
            processors.group_library_frames_processor,
            processors.remove_unnecessary_self_time_nodes,
            processors.remove_irrelevant_nodes,
        ]