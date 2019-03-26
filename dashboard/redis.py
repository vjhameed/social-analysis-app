import redis
from datetime import datetime



class UserAccountPair(object):
    AccountID = None
    UserId = None
    EndPoint = None



    def EncodeRequestQueueIdentifier(self):
        return 'T_RQ_'+str(self.UserId)+'_'+str(self.AccountID)
    @staticmethod
    def DecodeQueueIdentifier(Value):
        split = Value.split('_')
        p =UserAccountPair()
        p.UserId = int(split[2])
        p.PageId = int(split[3])
        p.EndPoint = int(split[4])
        return p

    def EncodeHourlyQueueIdentifier(self):
        return 'T_HQ_'+str(self.UserId)+'_'+str(self.AccountID)+'_'+str(self.EndPoint)

    def EncodeMaxLimitIdentifier(self):
        return 'T_LMT_'+str(self.UserId)+'_'+str(self.AccountID)+'_'+str(self.EndPoint)

    def EncodeMaxLimitExpireIdentifier(self):
        return 'T_EHLMT_'+str(self.UserId)+'_'+str(self.AccountID)+'_'+str(self.EndPoint)





class UserAccountRequestPair(UserAccountPair):
    RequestId = None
    SubRequestId = None

    @staticmethod
    def DecodeHQExpireHelper(Value):
        print('Decode String')
        print(Value)
        split = Value.split('_')
        p = UserAccountRequestPair()
        p.UserId = int(split[2])
        p.AccountID = split[3]
        p.EndPoint = split[4]
        p.RequestId = int(split[5])
        p.SubRequestId = int(split[6])
        return p

    def EncodeHQExpireHelper(self):
        return 'T_EHHQ_'+str(self.UserId)+'_'+str(self.AccountID)+'_'+str(self.EndPoint)+'_'+str(self.RequestId)+'_'+str(self.SubRequestId)



class TwitterManager(object):
    db = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)


    @staticmethod
    def RequestQueueHasItems(UserAccountPair):
        print(F'[{datetime.now()}] Request Queue String: {UserAccountPair.EncodeRequestQueueIdentifier()}')
        print(F'[{datetime.now()}] Request Queue Items Length: {TwitterManager.db.llen(UserAccountPair.EncodeRequestQueueIdentifier())}')
        return TwitterManager.db.llen(UserAccountPair.EncodeRequestQueueIdentifier()) > 0


    @staticmethod
    def DeQueueRequestMember(UserAccountRequestPair):
        print(F'[{datetime.now()}] DeQueueRequestMember: {UserAccountRequestPair.__dict__}')
        TwitterManager.db.rpoplpush(UserAccountRequestPair.EncodeRequestQueueIdentifier(), UserAccountRequestPair.EncodeHourlyQueueIdentifier())
        TwitterManager.db.set(UserAccountRequestPair.EncodeHQExpireHelper(), UserAccountRequestPair.RequestId, ex=900) #ex=3600

    @staticmethod
    def EnQueueTwitterRequest(UserAccountRequestPair):
        print(F'User Page Request Pair: {UserAccountRequestPair.__dict__}')
        CheckIfHQIsBellowLimit = TwitterManager.CheckIfHQIsBellowLimit(UserAccountRequestPair)
        print(F'[{datetime.now()}] HQ Bellow Limit: {CheckIfHQIsBellowLimit}')

        if TwitterManager.CheckIfHQIsBellowLimit(UserAccountRequestPair) and TwitterManager.SendRequest(UserAccountRequestPair):
            TwitterManager.PolulateHourlyQueue(UserAccountRequestPair)
        else:
            TwitterManager.PopulateRequestQueue(UserAccountRequestPair)

    @staticmethod
    def PopulateRequestQueue(UserAccountRequestPair):
        print(F'[{datetime.now()}] PopulateRequestQueue')
        TwitterManager.db.lpush(UserAccountRequestPair.EncodeRequestQueueIdentifier(), UserAccountRequestPair.RequestId)

    @staticmethod
    def CheckIfHQIsBellowLimit(UserAccountRequestPair):
        print(F'User Page Request Pair {UserAccountRequestPair.__dict__}')
        print(F'encode Max Limit Identifier: {UserAccountRequestPair.EncodeMaxLimitIdentifier()}')
        print(F'[{datetime.now()}] CheckIfHQIsBellowLimit {TwitterManager.db.get(UserAccountRequestPair.EncodeMaxLimitIdentifier()).decode("utf-8")} > {TwitterManager.db.llen(UserAccountRequestPair.EncodeHourlyQueueIdentifier())}')
        return int(TwitterManager.db.get(UserAccountRequestPair.EncodeMaxLimitIdentifier()).decode("utf-8")) > TwitterManager.db.llen(UserAccountRequestPair.EncodeHourlyQueueIdentifier())

    @staticmethod
    def PolulateHourlyQueue(UserAccountRequestPair):
        print(F'[{datetime.now()}] PolulateHourlyQueue')
        TwitterManager.db.lpush(UserAccountRequestPair.EncodeHourlyQueueIdentifier(), UserAccountRequestPair.RequestId)
        TwitterManager.db.set(UserAccountRequestPair.EncodeHQExpireHelper(), UserAccountRequestPair.RequestId, ex=900) #ex=3600

    @staticmethod
    def SetHourlyLimit(UserAccountPair):
        print(F'[{datetime.now()}] SetHourlyLimit: {UserAccountPair.__dict__}')
        EnguagementLimit = TwitterManager.GetEnguagementLimit(UserAccountPair)
        TwitterManager.db.set(UserAccountPair.EncodeMaxLimitIdentifier(),EnguagementLimit)
        TwitterManager.db.set(UserAccountPair.EncodeMaxLimitExpireIdentifier(), EnguagementLimit, ex=900) #ex=3600
        print(TwitterManager.db.ttl(UserAccountPair.EncodeMaxLimitExpireIdentifier()))

    @staticmethod
    def GetEnguagementLimit(UserAccountPair):
        return 2000



    @staticmethod
    def SendRequest(UserAccountRequestPairi):
        """
            All Sending Request Logic Hare
        """
        return True