import json
from flask              import Blueprint, Response, request

from gunpla_api.config  import Config
from gunpla_api.logger  import Logger

# from gunpla_api.utils   import Utils
from gunpla_api.controller  import Controller
from gunpla_api.validation  import Validation
from gunpla_api.gunpla_db   import GunplaDb
from gunpla_api.exceptions  import BadRequestException, DatabaseException, DatabaseUniqueException

logger  =  Logger().get_logger()
private =  Blueprint(
  'private',
  __name__,
  url_prefix='/api/private',
)

CONFIG =  Config()
CONTROLLER =  Controller()
VALIDATION =  Validation()
# UTILS  =  Utils()

# MAIN_CONTROLLER   =  MainController()


@private.route('/lifecheck',  methods=['GET'])
@private.route('/lifecheck/', methods=['GET', 'POST'])
def lifecheck():
  # MAIN_CONTROLLER.handle_auth(app.current_request)
  # print('request json: ', request.json)
  app_name     =  CONFIG.app_name
  logging_json =  { 'app_name': app_name }
  logger.info(logging_json)
    # if multiple qs for 'search'- params = request.args.getlist('search')
    # have request as dict = request.args.to_dict()
  return Response(
    response =  json.dumps({
      'appName' :  app_name,
      'stage'   :  CONFIG.stage,
      'path'    :  '/private/lifecheck',
      'status'  :  200,
    })
  )


@private.route('/db_post',  methods=['POST'])
@private.route('/db_post/', methods=['POST'])
def db_post_route():

  logger.info('request received')

  try:
    table = VALIDATION.get_json_field('table', request.json)
    logger.debug(f'insert request to table: {table}')
    if table == 'timeline':
      CONTROLLER.post_timeline(request)
    elif table == 'model_scale':
      CONTROLLER.post_model_scale(request)
    elif table == 'product_line':
      CONTROLLER.post_product_line(request)
    elif table == 'brand':
      CONTROLLER.post_brand(request)
    elif table == 'franchise':
      CONTROLLER.post_franchise(request)

    response = Response(status=200, response=json.dumps({'message': 'success'}))

  except BadRequestException as e:
    response = Response(status=400, response=json.dumps({'message': 'error'}))
  except DatabaseUniqueException as e:
    response = Response(status=400, response=json.dumps({'message': 'bad request'}))
  except DatabaseException as e:
    response = Response(status=500, response=json.dumps({'message': 'error'}))
  except Exception as e:
    logger.exception('unknown error occured')
    response = Response(status=400, response=json.dumps({'message': 'error'}))

  logger.info('request complete')
  return response


@private.route('/db_get',  methods=['GET'])
@private.route('/db_get/', methods=['GET'])
def db_get_route():
  logger.info('request received')

  try:
    table =  request.args['table']

    if table == 'timeline':
      json_data = CONTROLLER.get_timelines()

    response =  Response(status=200, response=json.dumps(json_data))
  except Exception as e:
    logger.exception('unknown error occured')
    response = Response(status=400, response=json.dumps({'message': 'error'}))

  logger.info('request complete')
  return response
