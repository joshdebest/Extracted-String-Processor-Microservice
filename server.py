import time
from wsgiref import simple_server
import falcon
import msgpack
import extracted_string_processor_handler


class CommunicationToBulkDataCollectorMicroservice:

    print("---------- EXTRACTED STRING PROCESSOR HAS SUCCESSFULLY STARTED ----------")

    def on_get(self, req, resp):
        """Handles GET requests"""
        outgoing_message = {"msg": "A Successful Connection made to extracted-string-processor API Server"}
        # TODO Eventually make outgoing message encoded
        resp.data = msgpack.packb(outgoing_message)
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_200
        print(resp)

    def on_post(self, req, resp):
        raw_incoming_message_command = req.media.get('command')
        print(raw_incoming_message_command)
        if raw_incoming_message_command == "StartExtractedStringProcessorMicroservice":
            outgoing_message = {'msg': 'Starting OCR Processing Microservice'}
            # TODO Eventually make outgoing message encoded
            resp.data = msgpack.packb(outgoing_message)
            resp.content_type = falcon.MEDIA_JSON
            resp.status = falcon.HTTP_200
            print(resp)
            start_time = time.time()
            extracted_string_processor_handler.start_extraction_string_processor()
            print("\n*---- Processing all tiff files took", time.time() - start_time, "seconds to run ----*")
        else:
            outgoing_message = {"msg": "A Successful Connection has been made to Extracted-String-Processor"}
            resp.data = msgpack.packb(outgoing_message)
            resp.content_type = falcon.MEDIA_JSON
            resp.status = falcon.HTTP_406
            print(resp)


api = falcon.API()
api.add_route('/', CommunicationToBulkDataCollectorMicroservice())

if __name__ == '__main__':
    httpd = simple_server.make_server('', 8090, api)
    httpd.serve_forever()
