#!/usr/bin/env python3
from urllib.parse import urlencode
from urllib.request import urlopen
from xml.dom.minidom import parse # type: ignore


# https://www.goodreads.com/api
# TODO maybe add these too?
# auth.user   —   Get id of user who authorized OAuth.
# group.list   —   List groups for a given user.
# owned_books.list   —   List books owned by a user.
# reviews.list   —   Get the books on a members shelf.
# review.show   —   Get a review.
# review.show_by_user_and_book   —   Get a user's review for a given book.
# shelves.list   —   Get a user's shelves.
# user.show   —   Get info about a member by id or username.
# user.compare   —   Compare books with another member.
# user.followers   —   Get a user's followers.
# user.following   —   Get people a user is following.
# user.friends   —   Get a user's friends.

class Exporter:
    def __init__(self, *args, **kwargs) -> None:
        self.base_url = 'https://www.goodreads.com/'
        self.user = kwargs['user']
        self.key = kwargs['key']
        self.per_page = 100 # TODO FIXME 200

    # apparently no json... https://www.goodreads.com/topic/show/1663342-json-endpoints
    def _get(self, endpoint: str, **kwargs):
        current_page = 1
        total = None

        results = [] # type: ignore
        while total is None or len(results) < total:
            query = urlencode([ # type: ignore
                ('v', '2'), ('key', self.key), ('per_page', self.per_page), ('page', current_page), *kwargs.items(),
            ])
            url = self.base_url + endpoint + '.xml?' + query
            chunk = parse(urlopen(url))

            [curr] = chunk.getElementsByTagName('reviews')
            total = int(curr.getAttribute('total'))
            results.extend(curr.getElementsByTagName('review'))
            current_page += 1
            # TODO user id??
        return results


    def export_xmll(self):
        for endpoint in ['review/list']:
            reviews = self._get(endpoint, id=self.user)
            for r in reviews:
                print(r.toxml())


def get_xmll(**params):
    return Exporter(**params).export_xmll()


def main():
    from export_helper import setup_parser
    import argparse
    parser = argparse.ArgumentParser('Export/takeout for your personal Goodreads data')
    setup_parser(parser=parser, params=['user', 'key'])
    args = parser.parse_args()

    params = args.params
    dumper = args.dumper

    x = get_xmll(**params)
    # dumper()
    return


if __name__ == '__main__':
    main()
