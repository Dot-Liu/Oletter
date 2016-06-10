#!/usr/bin/python
#-*- coding: utf8 -*-

import web

from route import route
from database import *
from output import output

@route('/api/user/disconnect')

class UserDisconnect:
    def POST(self):
        session = web.ctx.session
        if not session.have_key('user_id'):
            return output(411)
        if session['user_type'] == '0':
            return output(410)
        db = getDb()

        user={'id':session['user_id']}
        result = db.select('mate',user,
                           where = 'user_id=$id',
                           what = 'mate_id')
        res = result[0]
        t = db.transaction()
        try:
            db.update('userinfo',user,
                      where = 'user_id=$id',have_connect= '0')
            db.update('userinfo',var={'id':res.mate_id},
                      where = 'user_id=$id',have_connect = '0')
            t.commit()
        except:
            t.rollback()
            return output(700)
        return output(200)