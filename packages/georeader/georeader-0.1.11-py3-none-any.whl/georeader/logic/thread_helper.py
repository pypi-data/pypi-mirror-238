import concurrent.futures
import requests
import threading

thread_local = threading.local()


def get_session():
    """
    Returns:
        The current thread's session
    """
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def download_site(params):
    """
    The download_site function downloads the contents of a URL and returns its length.

    Args:
        params: Pass a list of parameters to the function

    Returns:
        The response object from the get() method
    """
    url = params[0]
    session = get_session()
    with session.get(url) as response:
        print(f"Read {len(response.content)} from {url}")


def threadpool_download(dl_func, params):
    """
    The threadpool_download function accepts a download function and list of parameters as input.
    It then creates a threadpool with 5 threads, and for each parameter in the list, it executes the
    download function on that parameter. The output is returned as a generator object.

    Args:
        dl_func: Specify the function that will be called for each of the items in params
        params: Pass the parameters to the download function

    Returns:
        A list of futures
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(dl_func, params)
