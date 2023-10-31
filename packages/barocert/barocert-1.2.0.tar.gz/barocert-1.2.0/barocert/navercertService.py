# -*- coding: utf-8 -*-
# Module for NavercertService API. It include base functionality of the
# RESTful web service request and parse json result. It uses Linkhub module
# to accomplish authentication APIs.
#
# 
# Author : linkhub dev
# Written : 2023-10-31
# Thanks for your interest.

from .base import BaseService, BarocertException

class NavercertService(BaseService):
    def __init__(self, LinkID, SecretKey, timeOut=15):
        """ 생성자.
            args
                LinkID : 링크허브에서 발급받은 LinkID
                SecretKey : 링크허브에서 발급받은 SecretKey
        """
        super(self.__class__, self).__init__(LinkID, SecretKey)
        self._addScope("421")
        self._addScope("422")
        self._addScope("423")
    
    # 본인인증 요청
    def requestIdentity(self, clientCode, identity):

        if clientCode == None or clientCode == "":
            raise BarocertException(-99999999, "이용기관코드가 입력되지 않았습니다.")
        if False == clientCode.isdigit():
            raise BarocertException(-99999999, "이용기관코드는 숫자만 입력할 수 있습니다.")
        if 12 != len(clientCode):
            raise BarocertException(-99999999, "이용기관코드는 12자 입니다.")
        if identity == None or identity == "":
            raise BarocertException(-99999999, "본인인증 서명요청 정보가 입력되지 않았습니다.")    
        if identity.receiverHP == None or identity.receiverHP == "":
            raise BarocertException(-99999999, "수신자 휴대폰번호가 입력되지 않았습니다.")
        if identity.receiverName == None or identity.receiverName == "":
            raise BarocertException(-99999999, "수신자 성명이 입력되지 않았습니다.")
        if identity.receiverBirthday == None or identity.receiverBirthday == "":
            raise BarocertException(-99999999, "생년월일이 입력되지 않았습니다.")
        if identity.expireIn == None or identity.expireIn == "":
            raise BarocertException(-99999999, "만료시간이 입력되지 않았습니다.")
        
        postData = self._stringtify(identity)

        return self._httppost('/NAVER/Identity/' + clientCode, postData)

    # 본인인증 상태확인
    def getIdentityStatus(self, clientCode, receiptId):

        if clientCode == None or clientCode == "":
            raise BarocertException(-99999999, "이용기관코드가 입력되지 않았습니다.")
        if False == clientCode.isdigit():
            raise BarocertException(-99999999, "이용기관코드는 숫자만 입력할 수 있습니다.")
        if 12 != len(clientCode):
            raise BarocertException(-99999999, "이용기관코드는 12자 입니다.")
        if receiptId == None or receiptId == "":
            raise BarocertException(-99999999, "접수아이디가 입력되지 않았습니다.")
        if False == receiptId.isdigit():
            raise BarocertException(-99999999, "접수아이디는 숫자만 입력할 수 있습니다.")
        if 32 != len(receiptId):
            raise BarocertException(-99999999, "접수아이디는 32자 입니다.")
        

        return self._httpget('/NAVER/Identity/' + clientCode + '/' + receiptId )
    
    # 본인인증 검증
    def verifyIdentity(self, clientCode, receiptId):

        if clientCode == None or clientCode == "":
            raise BarocertException(-99999999, "이용기관코드가 입력되지 않았습니다.")
        if False == clientCode.isdigit():
            raise BarocertException(-99999999, "이용기관코드는 숫자만 입력할 수 있습니다.")
        if 12 != len(clientCode):
            raise BarocertException(-99999999, "이용기관코드는 12자 입니다.")
        if receiptId == None or receiptId == "":
            raise BarocertException(-99999999, "접수아이디가 입력되지 않았습니다.")
        if False == receiptId.isdigit():
            raise BarocertException(-99999999, "접수아이디는 숫자만 입력할 수 있습니다.")
        if 32 != len(receiptId):
            raise BarocertException(-99999999, "접수아이디는 32자 입니다.")

        return self._httppost('/NAVER/Identity/' + clientCode + '/' + receiptId )

    # 전자서명 요청(단건)
    def requestSign(self, clientCode, sign):

        if clientCode == None or clientCode == "":
            raise BarocertException(-99999999, "이용기관코드가 입력되지 않았습니다.")
        if False == clientCode.isdigit():
            raise BarocertException(-99999999, "이용기관코드는 숫자만 입력할 수 있습니다.")
        if 12 != len(clientCode):
            raise BarocertException(-99999999, "이용기관코드는 12자 입니다.")
        if sign == None or sign == "":
            raise BarocertException(-99999999, "전자서명 요청정보가 입력되지 않았습니다.")
        if sign.receiverHP == None or sign.receiverHP == "":
            raise BarocertException(-99999999, "수신자 휴대폰번호가 입력되지 않았습니다.")
        if sign.receiverName == None or sign.receiverName == "":
            raise BarocertException(-99999999, "수신자 성명이 입력되지 않았습니다.")
        if sign.receiverBirthday == None or sign.receiverBirthday == "":
            raise BarocertException(-99999999, "생년월일이 입력되지 않았습니다.")
        if sign.reqTitle == None or sign.reqTitle == "":
            raise BarocertException(-99999999, "인증요청 메시지 제목이 입력되지 않았습니다.")
        if sign.reqMessage == None or sign.reqMessage == "":
            raise BarocertException(-99999999, "인증요청 메시지가 입력되지 않았습니다.")
        if sign.callCenterNum == None or sign.callCenterNum == "":
            raise BarocertException(-99999999, "고객센터 연락처가 입력되지 않았습니다.")
        if sign.expireIn == None or sign.expireIn == "":
            raise BarocertException(-99999999, "만료시간이 입력되지 않았습니다.")
        if sign.token == None or sign.token == "":
            raise BarocertException(-99999999, "토큰 원문이 입력되지 않았습니다.")
        if sign.tokenType == None or sign.tokenType == "":
            raise BarocertException(-99999999, "원문 유형이 입력되지 않았습니다.")
        
        postData = self._stringtify(sign)

        return self._httppost('/NAVER/Sign/' + clientCode, postData)

    # 전자서명 상태확인(단건)
    def getSignStatus(self, clientCode, receiptId):

        if clientCode == None or clientCode == "":
            raise BarocertException(-99999999, "이용기관코드가 입력되지 않았습니다.")
        if False == clientCode.isdigit():
            raise BarocertException(-99999999, "이용기관코드는 숫자만 입력할 수 있습니다.")
        if 12 != len(clientCode):
            raise BarocertException(-99999999, "이용기관코드는 12자 입니다.")
        if receiptId == None or receiptId == "":
            raise BarocertException(-99999999, "접수아이디가 입력되지 않았습니다.")
        if False == receiptId.isdigit():
            raise BarocertException(-99999999, "접수아이디는 숫자만 입력할 수 있습니다.")
        if 32 != len(receiptId):
            raise BarocertException(-99999999, "접수아이디는 32자 입니다.")

        return self._httpget('/NAVER/Sign/' + clientCode + '/' + receiptId)

    # 전자서명 검증(단건)
    def verifySign(self, clientCode, receiptId):

        if clientCode == None or clientCode == "":
            raise BarocertException(-99999999, "이용기관코드가 입력되지 않았습니다.")
        if False == clientCode.isdigit():
            raise BarocertException(-99999999, "이용기관코드는 숫자만 입력할 수 있습니다.")
        if 12 != len(clientCode):
            raise BarocertException(-99999999, "이용기관코드는 12자 입니다.")
        if receiptId == None or receiptId == "":
            raise BarocertException(-99999999, "접수아이디가 입력되지 않았습니다.")
        if False == receiptId.isdigit():
            raise BarocertException(-99999999, "접수아이디는 숫자만 입력할 수 있습니다.")
        if 32 != len(receiptId):
            raise BarocertException(-99999999, "접수아이디는 32자 입니다.")

        return self._httppost('/NAVER/Sign/' + clientCode + '/' + receiptId)
    
    # 전자서명 요청(복수)
    def requestMultiSign(self, clientCode, multiSign):

        if clientCode == None or clientCode == "":
            raise BarocertException(-99999999, "이용기관코드가 입력되지 않았습니다.")
        if False == clientCode.isdigit():
            raise BarocertException(-99999999, "이용기관코드는 숫자만 입력할 수 있습니다.")
        if 12 != len(clientCode):
            raise BarocertException(-99999999, "이용기관코드는 12자 입니다.")
        if multiSign == None or multiSign == "":
            raise BarocertException(-99999999, "전자서명 요청정보가 입력되지 않았습니다.")
        if multiSign.receiverHP == None or multiSign.receiverHP == "":
            raise BarocertException(-99999999, "수신자 휴대폰번호가 입력되지 않았습니다.")
        if multiSign.receiverName == None or multiSign.receiverName == "":
            raise BarocertException(-99999999, "수신자 성명이 입력되지 않았습니다.")
        if multiSign.receiverBirthday == None or multiSign.receiverBirthday == "":
            raise BarocertException(-99999999, "생년월일이 입력되지 않았습니다.")
        if multiSign.reqTitle == None or multiSign.reqTitle == "":
            raise BarocertException(-99999999, "인증요청 메시지 제목이 입력되지 않았습니다.")
        if multiSign.reqMessage == None or multiSign.reqMessage == "":
            raise BarocertException(-99999999, "인증요청 메시지가 입력되지 않았습니다.")
        if multiSign.callCenterNum == None or multiSign.callCenterNum == "":
            raise BarocertException(-99999999, "고객센터 연락처가 입력되지 않았습니다.")
        if multiSign.expireIn == None or multiSign.expireIn == "":
            raise BarocertException(-99999999, "만료시간이 입력되지 않았습니다.")
        if self._isNullorEmptyToken(multiSign.tokens):
            raise BarocertException(-99999999, "토큰 원문이 입력되지 않았습니다.")
        if self._isNullorEmptyTokenType(multiSign.tokens):
            raise BarocertException(-99999999, "원문 유형이 입력되지 않았습니다.")

        postData = self._stringtify(multiSign)

        return self._httppost('/NAVER/MultiSign/' + clientCode, postData)

    # 전자서명 상태확인(복수)	
    def getMultiSignStatus(self, clientCode, receiptId):

        if clientCode == None or clientCode == "":
            raise BarocertException(-99999999, "이용기관코드가 입력되지 않았습니다.")
        if False == clientCode.isdigit():
            raise BarocertException(-99999999, "이용기관코드는 숫자만 입력할 수 있습니다.")
        if 12 != len(clientCode):
            raise BarocertException(-99999999, "이용기관코드는 12자 입니다.")
        if receiptId == None or receiptId == "":
            raise BarocertException(-99999999, "접수아이디가 입력되지 않았습니다.")
        if False == receiptId.isdigit():
            raise BarocertException(-99999999, "접수아이디는 숫자만 입력할 수 있습니다.")
        if 32 != len(receiptId):
            raise BarocertException(-99999999, "접수아이디는 32자 입니다.")

        return self._httpget('/NAVER/MultiSign/' + clientCode + '/' + receiptId)


    # 전자서명 검증(복수)
    def verifyMultiSign(self, clientCode, receiptId):

        if clientCode == None or clientCode == "":
            raise BarocertException(-99999999, "이용기관코드가 입력되지 않았습니다.")
        if False == clientCode.isdigit():
            raise BarocertException(-99999999, "이용기관코드는 숫자만 입력할 수 있습니다.")
        if 12 != len(clientCode):
            raise BarocertException(-99999999, "이용기관코드는 12자 입니다.")
        if receiptId == None or receiptId == "":
            raise BarocertException(-99999999, "접수아이디가 입력되지 않았습니다.")
        if False == receiptId.isdigit():
            raise BarocertException(-99999999, "접수아이디는 숫자만 입력할 수 있습니다.")
        if 32 != len(receiptId):
            raise BarocertException(-99999999, "접수아이디는 32자 입니다.")
        
        return self._httppost('/NAVER/MultiSign/' + clientCode + '/' + receiptId)

    def _isNullorEmptyTokenType(self, multiSignTokens):
        if multiSignTokens == None or multiSignTokens == "":
            return True
        if len(multiSignTokens) == 0:
            return True
        for multiSignToken in multiSignTokens:
            if multiSignToken.tokenType == None or multiSignToken.tokenType == "":
                return True
        return False
    
    def _isNullorEmptyToken(self, multiSignTokens):
        if multiSignTokens == None or multiSignTokens == "":
            return True
        if len(multiSignTokens) == 0:
            return True
        for multiSignToken in multiSignTokens:
            if multiSignToken.token == None or multiSignToken.token == "":
                return True
        return False


class NaverIdentity(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs
        
class NaverSign(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs

class NaverMultiSign(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs

class NaverMultiSignTokens(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs
