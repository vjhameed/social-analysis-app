import redis
from datetime import datetime
from facebook.models import *
from dashboard.utils import *
from jsonmerge import merge
import json


class UserPagePair(object):
    PageId = None
    UserId = None



    def EncodeRequestQueueIdentifier(self):
        return 'F_RQ_'+str(self.UserId)+'_'+str(self.PageId)
    @staticmethod
    def DecodeQueueIdentifier(Value):
        split = Value.split('_')
        p =UserPagePair()
        p.UserId = int(split[2])
        p.PageId = int(split[3])
        return p

    def EncodeHourlyQueueIdentifier(self):
        return 'F_HQ_'+str(self.UserId)+'_'+str(self.PageId)

    def EncodeMaxLimitIdentifier(self):
        return 'F_LMT_'+str(self.UserId)+'_'+str(self.PageId)

    def EncodeMaxLimitExpireIdentifier(self):
        return 'F_EHLMT_'+str(self.UserId)+'_'+str(self.PageId)

class UserPageRequestPair(UserPagePair):
    RequestId = None
    SubRequestId = None
    CommentID = None

    @staticmethod
    def DecodeHQExpireHelper(Value):
        print('Decode String')
        print(Value)
        split = Value.split('_')
        p = UserPageRequestPair()
        p.UserId = int(split[2])
        p.PageId = split[3]
        p.RequestId = int(split[4])
        p.SubRequestId = int(split[5])
        return p

    def EncodeHQExpireHelper(self):
        return 'F_EHHQ_'+str(self.UserId)+'_'+str(self.PageId)+'_'+str(self.RequestId)+'_'+str(self.SubRequestId)


class FacebookManager:



    db = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)




    @staticmethod
    def RequestQueueHasItems(UserPagePair):
        print(F'[{datetime.now()}] Request Queue String: {UserPagePair.EncodeRequestQueueIdentifier()}')
        print(F'[{datetime.now()}] Request Queue Items Length: {FacebookManager.db.llen(UserPagePair.EncodeRequestQueueIdentifier())}')
        return FacebookManager.db.llen(UserPagePair.EncodeRequestQueueIdentifier()) > 0

    @staticmethod
    def DeQueueRequestMember(UserPageRequestPair):
        print(F'[{datetime.now()}] DeQueueRequestMember: {UserPageRequestPair.__dict__}')
        FacebookManager.db.rpoplpush(UserPageRequestPair.EncodeRequestQueueIdentifier(), UserPageRequestPair.EncodeHourlyQueueIdentifier())
        FacebookManager.db.set(UserPageRequestPair.EncodeHQExpireHelper(), UserPageRequestPair.RequestId, ex=3600) #ex=3600

    @staticmethod
    def EnQueueFacebookRequest(UserPageRequestPair):
        print(F'User Page Request Pair: {UserPageRequestPair.__dict__}')
        CheckIfHQIsBellowLimit = FacebookManager.CheckIfHQIsBellowLimit(UserPageRequestPair)
        print(F'[{datetime.now()}] HQ Bellow Limit: {CheckIfHQIsBellowLimit}')

        if FacebookManager.CheckIfHQIsBellowLimit(UserPageRequestPair) and FacebookManager.SendRequest(UserPageRequestPair):
            FacebookManager.PolulateHourlyQueue(UserPageRequestPair)
        else:
            FacebookManager.PopulateRequestQueue(UserPageRequestPair)

    @staticmethod
    def PopulateRequestQueue(UserPageRequestPair):
        print(F'[{datetime.now()}] PopulateRequestQueue')
        FacebookManager.db.lpush(UserPageRequestPair.EncodeRequestQueueIdentifier(), UserPageRequestPair.RequestId)

    @staticmethod
    def CheckIfHQIsBellowLimit(UserPageRequestPair):
        print(F'User Page Request Pair {UserPageRequestPair.__dict__}')
        print(F'encode Max Limit Identifier: {UserPageRequestPair.EncodeMaxLimitIdentifier()}')
        print(F'[{datetime.now()}] CheckIfHQIsBellowLimit {FacebookManager.db.get(UserPageRequestPair.EncodeMaxLimitIdentifier()).decode("utf-8")} > {FacebookManager.db.llen(UserPageRequestPair.EncodeHourlyQueueIdentifier())}')
        return int(FacebookManager.db.get(UserPageRequestPair.EncodeMaxLimitIdentifier()).decode("utf-8")) > FacebookManager.db.llen(UserPageRequestPair.EncodeHourlyQueueIdentifier())

    @staticmethod
    def PolulateHourlyQueue(UserPageRequestPair):
        print(F'[{datetime.now()}] PolulateHourlyQueue')
        FacebookManager.db.lpush(UserPageRequestPair.EncodeHourlyQueueIdentifier(), UserPageRequestPair.RequestId)
        FacebookManager.db.set(UserPageRequestPair.EncodeHQExpireHelper(), UserPageRequestPair.RequestId, ex=3600) #ex=3600

    @staticmethod
    def SetHourlyLimit(UserPagePair):
        print(F'[{datetime.now()}] SetHourlyLimit: {UserPagePair.__dict__}')
        EnguagementLimit = FacebookManager.GetEnguagementLimit(UserPagePair)
        # print(F'[{datetime.now()}] Got Limit: {EnguagementLimit}')
        FacebookManager.db.set(UserPagePair.EncodeMaxLimitIdentifier(),EnguagementLimit)
        FacebookManager.db.set(UserPagePair.EncodeMaxLimitExpireIdentifier(), EnguagementLimit, ex=3600) #ex=3600
        print(FacebookManager.db.ttl(UserPagePair.EncodeMaxLimitExpireIdentifier()))

    @staticmethod
    def GetEnguagementLimit(UserPagePair):
        return 2000



    @staticmethod
    def SendRequest(UserPageRequestPairi):
        """
            All Sending Request Logic Hare
        """
        return True

