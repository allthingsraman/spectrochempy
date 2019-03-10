# -*- coding: utf-8 -*-
#
# ======================================================================================================================
# Copyright (©) 2015-2019 LCS
# Laboratoire Catalyse et Spectrochimie, Caen, France.
# CeCILL-B FREE SOFTWARE LICENSE AGREEMENT  
# See full LICENSE agreement in the root directory
# ======================================================================================================================

import logging
from spectrochempy import log, WARNING, INFO, set_loglevel

def test_logger(caplog):

    log = logging.getLogger('SpectroChemPy')
    log.propagate = True
    caplog.set_level(logging.DEBUG)

    # We can set the level using strings
    set_loglevel("DEBUG")
    assert log.level == logging.DEBUG

    set_loglevel(WARNING)
    assert log.level == logging.WARNING

    log.error('\n'+'*' * 80+'\n')
    log.debug('debug in WARNING level - should not appear')
    log.info('info in WARNING level - should not appear')
    log.warning('OK this is a Warning')
    log.error('OK This is an Error')

    log.error('\n' + '*' * 80 + '\n')

    set_loglevel(INFO)
    assert log.level == logging.INFO

    log.debug('debug in INFO level - should not appear')
    log.info('OK - info in INFO level')
    log.warning('OK this is a Warning')
    log.error('OK This is an Error')

    log.error('\n' + '*' * 80 + '\n')

    set_loglevel('DEBUG')
    assert log.level == logging.DEBUG

    log.debug('OK - debug in DEBUG level')
    log.info('OK - info in DEBUG level')
    assert caplog.records[-1].levelname == 'INFO'
    assert caplog.records[-1].message == 'OK - info in DEBUG level'
    log.warning('OK this is a Warning')
    assert caplog.records[-1].levelname == 'WARNING'
    assert caplog.records[-1].message == 'OK this is a Warning'
    log.error('OK This is an Error')
    assert caplog.records[-1].levelname == 'ERROR'
    assert caplog.records[-1].message == 'OK This is an Error'
