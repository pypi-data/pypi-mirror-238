import os
from setuptools import setup, find_packages

base_dir = os.path.dirname(os.path.abspath(__file__))
docs_path = os.path.join(base_dir, 'docs.md')

setup(
    name='hanime',
    version='1.0.1',
    description='A simple Python wrapper for interacting with Hanime\'s API.',
    author='dancers.',
    author_email='bio@fbi.ac',
    url='https://github.com/lolpuud/hanime',
    packages=find_packages(include=['hanime*']),
    install_requires=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    long_description="""## Introduction

The `Hanime` Python Library allows you to interact with `Hanime`'s API, fetching information about videos, images, channels, and performing searches. You can use this library to build applications or tools that make use of `Hanime`'s data. The library is designed to be easy to use and provides a variety of features.

## Requirements

Before using this library, you should ensure that you have the following requirements:

- Python 3.6 or later
- Requests library (`pip install requests`)
- Beautiful Soup library (`pip install beautifulsoup4`)

## Table of Contents

1. [`HanimeUser` Class](#hanimeuser-class)
2. [`UserClient` Class](#userclient-class)
    - [`BASE_URL` Class Attribute](#base-url-class-attribute)
    - [`__init__(self, cookies={'in_d4': '1', 'in_m4': '1'}, headers={})` Method](#init-method)
    - [`create_default_headers()` Method](#create-default-headers-method)
    - [`get_channel_info(channel_id)` Method](#get-channel-info-channel_id-method)

3. [`HanimeImage` Data Class](#hanimeimage-data-class)
4. [`ImageClient` Class](#imageclient-class)
    - [`create_default_headers()` Method](#create-default-headers-method)
    - [`build_query(channel_names: List[str], offset: int)` Method](#build-query-channel_names-liststroffset-int-method)
    - [`parse_community_uploads(data: dict)` Method](#parse-community-uploadsdata-dict-method)
    - [`get_community_uploads(channel_names: List[str], offset: int)` Method](#get-community-uploads-channel_names-liststroffset-int-method)

5. [`SearchPayload` Data Class](#searchpayload-data-class)
    - [`create_default_payload()` Method](#create-default-payload-method)
    - [`convert_ordering(ordering)` Method](#convert-ordering-ordering-method)
    - [`convert_order_by(order_by)` Method](#convert-order-by-order_by-method)

6. [`BaseSearchHeaders` Data Class](#basesearchheaders-data-class)
    - [`create_default_headers()` Method](#create-default-headers-method)

7. [`ParsedData` Class](#parseddata-class)
8. [`SearchClient` Class](#searchclient-class)
    - [`__init__(client_identifier=None)` Method](#init-client_identifiernone-method)
    - [`search(payload)` Method](#search-payload-method)
    - [`filter_response(base_response, filter_options)` Method](#filter-responsebase_response-filter_options-method)
    - [`parse_hits_data(response)` Method](#parse-hits-dataresponse-method)

9. [`HanimeVideo` Class](#hanimevideo-class)
10. [`VideoClient` Class](#videoclient-class)
    - [`BASE_URL` Class Attribute](#base-url-class-attribute)
    - [`TAGS` Class Attribute](#tags-class-attribute)
    - [`__init__(self, cookies={'in_d4': '1', 'in_m4': '1',}, client_identifier=None)` Method](#init-method)
    - [`create_default_headers(client_identifier: str = None)` Method](#create-default-headers-method)
    - [`get_video_info(video_id)` Method](#get-video-info-video_id-method)
    - [`get_random_video()` Method](#get-random-video-method)
    - [`get_random_video_tag(num_tags: int = 1, include_tags: Optional[List[str]] = None, exclude_tags: Optional[List[str]] = None)` Method](#get-random-video-tag-num_tags-int--1-include_tags-optionalliststr--none-exclude_tags-optionalliststr--none-method)
  
## `HanimeImage` (Data Class)

`HanimeImage` is a data class used to represent information about an image from Hanime. It contains the following attributes:

- `id` (int): The unique identifier for the image.
- `channel_name` (str): The name of the channel associated with the image.
- `username` (str): The username of the uploader.
- `url` (str): The URL of the image.
- `proxy_url` (str): The proxy URL of the image.
- `extension` (str): The file extension of the image (e.g., "jpg", "png").
- `width` (int): The width of the image in pixels.
- `height` (int): The height of the image in pixels.
- `filesize` (int): The size of the image file in bytes.
- `created_at_unix` (int): The timestamp when the image was created in Unix time format.
- `updated_at_unix` (int): The timestamp when the image was last updated in Unix time format.
- `discord_user_id` (str): The Discord user ID associated with the image.
- `user_avatar_url` (str): The URL of the user's avatar.
- `canonical_url` (str): The canonical URL of the image.

## `ImageClient` Class

`ImageClient` is a class that provides methods for interacting with Hanime's community image uploads. It includes utility methods for building requests and parsing responses.

### `create_default_headers()` Method

This method returns a dictionary of default HTTP headers that can be used for making requests to Hanime's API.

Example:

```python
headers = ImageClient.create_default_headers()
```

### `build_query(channel_names: List[str], offset: int)` Method

This method builds a query dictionary for fetching community uploads based on channel names and an offset value.

- `channel_names` (List[str]): A list of channel names to filter the uploads.
- `offset` (int): The offset value for pagination.

Example:

```python
query = ImageClient.build_query(['channel1', 'channel2'], 10)
```

### `parse_community_uploads(data: dict)` Method

This method parses the data returned from a Hanime API response and returns a list of `HanimeImage` objects.

- `data` (dict): The API response data.

Example:

```python
data = {"data": [...] }  # API response data
images = ImageClient.parse_community_uploads(data)
```

### `get_community_uploads(channel_names: List[str], offset: int)` Method

This method makes an HTTP GET request to fetch community uploads based on channel names and an offset value.

- `channel_names` (List[str]): A list of channel names to filter the uploads.
- `offset` (int): The offset value for pagination.

Example:

```python
images_data = ImageClient.get_community_uploads(['channel1', 'channel2'], 10)
```

---

## `SearchPayload` (Data Class)

`SearchPayload` is a data class used to represent a payload for searching on Hanime. It contains the following attributes:

- `search_text` (str): The search text or query.
- `tags` (list): A list of tags to filter the search results.
- `tags_mode` (str): The mode for combining tags ("AND" or "OR").
- `brands` (list): A list of brands to filter the search results.
- `blacklist` (list): A list of items to blacklist from search results.
- `order_by` (str): The field to order search results by.
- `ordering` (str): The ordering direction for search results (e.g., "desc" for descending).
- `page` (int): The page number for paginating search results.

### `create_default_payload()` Method

This method creates a default payload with default values for searching.

Example:

```python
default_payload = SearchPayload.create_default_payload()
```

### `convert_ordering(ordering)` Method

This method converts an ordering option into the corresponding value used in the payload.

Example:

```python
ordering_value = SearchPayload.convert_ordering('recent_uploads')
```

### `convert_order_by(order_by)` Method

This method converts an order-by option into the corresponding value used in the payload.

Example:

```python
order_by_value = SearchPayload.convert_order_by('most_views')
```

## `BaseSearchHeaders` Data Class

`BaseSearchHeaders` is a data class used to represent HTTP headers for making search requests. It contains attributes for common HTTP headers.

### `create_default_headers()` Method

This method creates a default set of HTTP headers for making search requests.

Example:

```python
default_headers = BaseSearchHeaders.create_default_headers()
```

## `ParsedData` Class

`ParsedData` is a class used to parse and work with data returned in search responses. It provides a way to access attributes in a dictionary-like manner and parse HTML descriptions.

Example:

```python
parsed_data = ParsedData(data)
description = parsed_data.description
```

## `SearchClient` Class

`SearchClient` is a class that allows you to interact with Hanime's search functionality. It provides methods for searching, filtering responses, and parsing hits data.

### `__init__(client_identifier=None)` Method

This method initializes a `SearchClient` with an optional client identifier.

Example:

```python
search_client = SearchClient(client_identifier='my-client')
```

### `search(payload)` Method

This method sends a search request using the provided payload and returns the JSON response.

Example:

```python
search_payload = SearchPayload(search_text='hentai', tags=['tag1', 'tag2'])
response = search_client.search(search_payload)
```

### `filter_response(base_response, filter_options)` Method

This static method filters the response data based on specified filter options.

Example:

```python
filtered_response = SearchClient.filter_response(base_response, ['hits', 'total'])
```

### `parse_hits_data(response)` Method

This static method parses hits data from the response and returns a list of `ParsedData` objects.

Example:

```python
hits_data = SearchClient.parse_hits_data(response)
```

---

Here's the markdown documentation for the provided Python code:

## `HanimeUser` Class

`HanimeUser` is a class used to represent a user's information from Hanime. It is initialized with user data and provides a dynamic way to access user attributes.

### `__init__(self, data)` Method

- `data` (dict): User data containing various attributes.

Example:

```python
user_data = {"username": "example_user", "id": 12345, "avatar_url": "https://example.com/avatar.jpg"}
hanime_user = HanimeUser(user_data)
username = hanime_user.username
```

## `UserClient` Class

`UserClient` is a class that interacts with Hanime's user-related API endpoints. It provides methods for fetching user-related information.

### `BASE_URL` Class Attribute

- `BASE_URL` (str): The base URL for Hanime's API.

### `__init__(self, cookies={'in_d4': '1', 'in_m4': '1'}, headers={})` Method

- `cookies` (dict): Custom cookies to include in requests.
- `headers` (dict): Custom HTTP headers to include in requests.

Example:

```python
user_client = UserClient() # Leave cookies & headers as none, therefore the library can use the correct ones. Unless you have fresh ones, that work maybe with `x-signature`.
```

### `create_default_headers()` Method

This method returns a dictionary of default HTTP headers for making requests to Hanime's API.

Example:

```python
default_headers = UserClient.create_default_headers()
```

### `get_channel_info(channel_id)` Method

This method retrieves information about a Hanime channel based on the provided channel ID.

- `channel_id` (int): The ID of the channel to fetch information for.

Example:

```python
channel_info = user_client.get_channel_info('test-123')
```

The returned value is a `HanimeUser` object representing the channel's information.

In case of an error, the method will return `None`.

---

Here's the markdown documentation for the provided Python code:

## `HanimeVideo` Class

`HanimeVideo` is a class used to represent information about a video on Hanime. It is initialized with video data and provides a dynamic way to access video attributes.

### `__init__(self, data)` Method

- `data` (dict): Video data containing various attributes.

Example:

```python
video_data = {"title": "Example Video", "duration": 1200, "tags": ["tag1", "tag2"]}
hanime_video = HanimeVideo(video_data)
title = hanime_video.title
```

### `__getattr__(self, name)` Method

This method allows dynamic access to video attributes. It returns the value of the requested attribute if it exists in the video data.

Example:

```python
duration = hanime_video.duration
```

### `description` Property

This property parses and returns the description of the video from the HTML description provided in the data.

Example:

```python
description = hanime_video.description
```

## `VideoClient` Class

`VideoClient` is a class that interacts with Hanime's video-related API endpoints. It provides methods for fetching video information and random videos based on tags.

### `BASE_URL` Class Attribute

- `BASE_URL` (str): The base URL for Hanime's API.

### `TAGS` Class Attribute

- `TAGS` (List[str]): A list of valid tags used for filtering videos.

### `__init__(self, cookies={'in_d4': '1', 'in_m4': '1',}, client_identifier=None)` Method

- `cookies` (dict): Custom cookies to include in requests.
- `client_identifier` (str): An optional client identifier used in headers.

Example:

```python
video_client = VideoClient(client_identifier='my-client')
```

### `create_default_headers(client_identifier: str = None)` Method

This method returns a dictionary of default HTTP headers for making requests to Hanime's API. It allows you to include a client identifier in the headers.

Example:

```python
default_headers = VideoClient.create_default_headers(client_identifier='my-client')
```

### `get_video_info(video_id)` Method

This method retrieves information about a Hanime video based on the provided video ID.

- `video_id` (int): The ID of the video to fetch information for.

Example:

```python
video_info = video_client.get_video_info(123)
```

The returned value is a `HanimeVideo` object representing the video's information.

In case of an error, the method will return `None`.

### `get_random_video()` Method

This method fetches a random Hanime video.

Example:

```python
random_video = video_client.get_random_video()
```

The returned value is a `HanimeVideo` object representing the random video.

In case of an error, the method will return `None`.

### `get_random_video_tag(num_tags: int = 1, include_tags: Optional[List[str]] = None, exclude_tags: Optional[List[str]] = None)` Method

This method fetches a random Hanime video based on specified tags.

- `num_tags` (int): The number of tags to include in the search.
- `include_tags` (Optional[List[str]]): A list of tags to include in the search.
- `exclude_tags` (Optional[List[str]]): A list of tags to exclude from the search.

Example:

```python
random_video = video_client.get_random_video_tag(num_tags=3, include_tags=['tag1', 'tag2'])
```

The method returns a list of `ParsedData` objects representing the search results based on the specified tags.

In case of an error, the method will raise `InvalidTagsError` if invalid tags are provided or raise a `ValueError` if there are not enough valid tags available after filtering.

---

## Credits

- **Author:** [lolpuud](https://github.com/lolpuud)
    - **Discord:** `dancers.`
    - **Email:** `bio@fbi.ac`

## Author Note
```
I created this out of sheer boredom. However, this doesn't mean I won't update and maintain it. While it's not my top priority, I won't abandon the project. If there are issues that need fixing, I'll address them. I'll also work on new features if the need arises. I already have some plans for future updates, but for now, it's in good shape.

If you'd like to contribute, please feel free to create issues or pull requests. You can add new features, fix code, and more. I'll review them and accept if I find them beneficial or helpful :].
```
""",
    long_description_content_type='text/markdown',
)
