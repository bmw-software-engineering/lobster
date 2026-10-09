import json

from flask import Response

from tests_system.lobster_codebeamer.mock_server import create_app


if __name__ == '__main__':
    app = create_app()
    response_data = {
        'page': 1,
        'pageSize': 1,
        'total': 1,
        'items': [
            {
                'item': {
                    'id': 5,
                    'name': 'Requirement 5: Dynamic name',
                    'description': 'Dynamic description for requirement 5.',
                    'status': {
                        'id': 5,
                        'name': 'Status 5',
                        'type': 'ChoiceOptionReference'
                    },
                    'tracker': {
                        'id': 5,
                        'name': 'Tracker_Name_5',
                        'type': 'TrackerReference'
                    },
                    'version': 1
                }
            }
        ]
    }
    app.responses = [
        Response(json.dumps(response_data), status=200),
    ]
    app.start_server()
