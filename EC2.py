#!/usr/local/python3/bin/python3
# -*- coding: utf-8 -*-
__author__ = 'zhiyi'

#加载配置文件处理库
import configparser
#加载AWS库
import boto3
import pprint

#读取配置文件函数
def get_conf_dict(group):
    '''传入aws的组名，返回一个字典，
    该字典记录了boto登陆AWS所需要的信息
    调用方法列如
    get_conf_dict('oms')'''
    config_filename = 'aws.conf'
    cp = configparser.ConfigParser()
    cp.read(config_filename)
    if group in cp:
        cf_dict = {}
        cf_dict['aws_access_key_id']= cp[group]['aws_access_key_id']
        cf_dict['aws_secret_access_key']= cp[group]['aws_secret_access_key']
        cf_dict['region_name']= cp[group]['region_name']
        return cf_dict

#传入链接配置，返回链接函数闭包
def get_conn(**kwargs):
    def connect():
        aaki = kwargs['aws_access_key_id']
        asak = kwargs['aws_secret_access_key']
        rn = kwargs['region_name']
        return boto3.session.Session(aws_access_key_id=aaki,aws_secret_access_key=asak,region_name=rn)
    return connect

def list_ec2_vol(conn):
    client = conn().client('ec2')
    response = client.describe_instances()
    listec2vol = []
    for instances in response['Reservations']:
        for instance in instances['Instances']:
            insid, tag, ip, volid = instance['InstanceId'], instance['Tags'][0]['Value'], instance['PrivateIpAddress'],[ins['Ebs']['VolumeId'] for ins in instance['BlockDeviceMappings']]
            listec2vol.append([insid,tag,ip,volid])
    return listec2vol

def ec2_create_snapshot(conn,volid,descrip):
    client = conn().client('ec2')
    response = client.create_snapshot(VolumeId=volid,Description=descrip)
    print(response)


if __name__ == '__main__':
    conn_conf = get_conf_dict('oms')
    conn = get_conn(**conn_conf)
    print(list_ec2_vol(conn))
    conn2 = get_conn(**conn_conf)
    ec2_create_snapshot(conn2,'vol-ec025869','ops-20170509-python')