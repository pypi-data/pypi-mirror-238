from . import PipelineNode
from ..nonpublic import PipelineStatus

def _PipelineNode_compute(self, frame = None):
    """ Requests data from this pipeline node.

        The optional *frame* parameter determines the frame to retrieve, which must be in the range 0 through (:py:attr:`num_frames`-1).
        If you don't specify any frame number, the current time slider position will be used (always frame 0 for automation scripts not running in the context
        of an interactive OVITO session).

        The pipeline node uses a caching mechanism to keep the data for one or more trajectory frames in memory. Thus, invoking :py:meth:`!compute`
        repeatedly to retrieve the same frame will typically be very fast.

        :param int|None frame: The trajectory frame to retrieve or compute.
        :return: A new :py:class:`~ovito.data.DataCollection` containing the frame's data.
    """
    state = self._evaluate(frame)
    if state.status.type == PipelineStatus.Type.Error:
        raise RuntimeError(f"Data source evaluation failed: {state.status.text}")
    if state.data is None:
        raise RuntimeError("Data pipeline did not yield any output DataCollection.")

    return state.mutable_data

PipelineNode.compute = _PipelineNode_compute