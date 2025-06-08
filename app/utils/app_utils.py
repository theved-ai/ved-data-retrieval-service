from asgiref.sync import async_to_sync

def sync_stream_from_async(async_gen):
    # This function makes a sync generator out of your async generator
    agen = async_gen.__aiter__()

    def sync_gen():
        while True:
            try:
                chunk = async_to_sync(agen.__anext__)()
            except StopAsyncIteration:
                break
            yield chunk
    return sync_gen()
