#   Copyright ETH 2018 - 2023 Zürich, Scientific IT Services
# 
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
# 
#        http://www.apache.org/licenses/LICENSE-2.0
#   
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
import re
import time

import pytest

from pybis import Openbis


def test_token(openbis_instance):
    assert openbis_instance.token is not None
    assert openbis_instance.is_token_valid(openbis_instance.token) is True
    assert openbis_instance.is_session_active() is True


def http_only():
    with pytest.raises(Exception):
        new_instance = Openbis("http://localhost")
        assert new_instance is None

    new_instance = Openbis(
        url="http://localhost",
        allow_http_but_do_not_use_this_in_production_and_only_within_safe_networks=True,
    )
    assert new_instance is not None


def test_cached_token(other_openbis_instance):
    assert other_openbis_instance.is_token_valid() is True

    other_openbis_instance.logout()
    assert other_openbis_instance.is_token_valid() is False


def test_create_perm_id(openbis_instance):
    permId = openbis_instance.create_permId()
    assert permId is not None
    m = re.search("([0-9]){17}-([0-9]*)", permId)
    ts = m.group(0)
    assert ts is not None
    count = m.group(1)
    assert count is not None


def test_get_samples_update_in_transaction(openbis_instance):
    """
        Update samples in transaction without overriding parents/children
    """
    name_suffix = str(time.time())
    # Create new space
    space = openbis_instance.new_space(code='space_name' + name_suffix, description='')
    space.save()

    # Create new project
    project = space.new_project(code='project_code' + name_suffix)
    project.save()

    # Create new experiment
    experiment = openbis_instance.new_experiment(
        code='MY_NEW_EXPERIMENT',
        type='DEFAULT_EXPERIMENT',
        project=project.code
    )
    experiment.save()

    # Create parent sample
    sample1 = openbis_instance.new_sample(
        type='YEAST',
        space=space.code,
        experiment=experiment.identifier,
        parents=[],
        children=[],
        props={"$name": "sample1"}
    )
    sample1.save()

    # Create child sample
    sample2 = openbis_instance.new_sample(
        type='YEAST',
        space=space.code,
        experiment=experiment.identifier,
        parents=[sample1],
        children=[],
        props={"$name": "sample2"}
    )
    sample2.save()

    # Verify samples parent/child relationship
    sample1 = openbis_instance.get_sample(
        sample_ident=sample1.identifier,
        space=space.code,
        props="*"
    )
    sample2 = openbis_instance.get_sample(
        sample_ident=sample2.identifier,
        space=space.code,
        props="*"
    )
    assert sample1.children == [sample2.identifier]
    assert sample2.parents == [sample1.identifier]

    trans = openbis_instance.new_transaction()
    # get samples that have parents and update name
    samples = openbis_instance.get_samples(space=space.code, props="*", withParents="*")
    for sample in samples:
        sample.props["$name"] = 'new name for sample2'
        trans.add(sample)
    # get samples that have children and update name
    samples = openbis_instance.get_samples(space=space.code, props="*", withChildren="*")
    for sample in samples:
        sample.props["$name"] = 'new name for sample1'
        trans.add(sample)
    trans.commit()

    # Verify that name has been changed and parent/child relationship remains
    sample1 = openbis_instance.get_sample(
        sample_ident=sample1.identifier,
        space=space.code,
        props="*"
    )
    sample2 = openbis_instance.get_sample(
        sample_ident=sample2.identifier,
        space=space.code,
        props="*"
    )
    assert sample1.props["$name"] == 'new name for sample1'
    assert sample1.children == [sample2.identifier]
    assert sample2.props["$name"] == 'new name for sample2'
    assert sample2.parents == [sample1.identifier]

    trans = openbis_instance.new_transaction()
    # get samples with attributes and change name
    samples = openbis_instance.get_samples(space=space.code, attrs=["parents", "children"])
    for sample in samples:
        sample.props["$name"] = "default name"
        trans.add(sample)
    trans.commit()

    # Verify that name has been changed and parent/child relationship remains
    sample1 = openbis_instance.get_sample(
        sample_ident=sample1.identifier,
        space=space.code,
        props="*"
    )
    sample2 = openbis_instance.get_sample(
        sample_ident=sample2.identifier,
        space=space.code,
        props="*"
    )
    assert sample1.props["$name"] == 'default name'
    assert sample1.children == [sample2.identifier]
    assert sample2.props["$name"] == 'default name'
    assert sample2.parents == [sample1.identifier]

    sample3 = openbis_instance.new_sample(
        type='YEAST',
        space=space.code,
        experiment=experiment.identifier,
        parents=[],
        children=[],
        props={"$name": "sample3"}
    )
    sample3.save()

    trans = openbis_instance.new_transaction()
    # get sample1 without attributes and add sample3 as a parent
    samples = openbis_instance.get_samples(space=space.code, identifier=sample1.identifier)
    for sample in samples:
        sample.add_parents([sample3.identifier])
        trans.add(sample)
    # get sample2 without attributes and remove sample1 as a parent
    samples = openbis_instance.get_samples(space=space.code, identifier=sample2.identifier)
    for sample in samples:
        sample.del_parents([sample1.identifier])
        trans.add(sample)
    trans.commit()

    # Verify changes
    sample1 = openbis_instance.get_sample(
        sample_ident=sample1.identifier,
        space=space.code,
        props="*"
    )
    sample2 = openbis_instance.get_sample(
        sample_ident=sample2.identifier,
        space=space.code,
        props="*"
    )
    sample3 = openbis_instance.get_sample(
        sample_ident=sample3.identifier,
        space=space.code,
        props="*"
    )
    assert sample1.children == []
    assert sample1.parents == [sample3.identifier]
    assert sample2.parents == []
    assert sample3.children == [sample1.identifier]


def test_failed_second_login_raises_exception(openbis_instance):
    """
        Logins to openBIS using wrong username/password, PyBIS should raise exception
    """
    assert openbis_instance.is_session_active() is True

    try:
        openbis_instance.login('non_existing_username_for_test', 'abcdef')
        # Login should fail at this point
        assert False
    except ValueError as e:
        assert str(e) == "login to openBIS failed"


def test_set_token_accepts_personal_access_token_object(openbis_instance):
    """
        Verifies that set_token method accepts both permId and PersonalAccessToken object
    """
    assert openbis_instance.is_session_active() is True

    pat = openbis_instance.get_or_create_personal_access_token(sessionName="Project A")

    openbis_instance.set_token(pat, save_token=True)
    openbis_instance.set_token(pat.permId, save_token=True)



def test_upload():

    from pybis import Openbis
    def get_instance():
        # base_url = "http://localhost:8888/openbis"
        base_url = "https://alaskowski:8443/openbis"
        # base_url = "https://openbis-eln-studer.ethz.ch"
        # base_url = "https://openbis-sis-ci-sprint.ethz.ch/"
        # base_url = "https://openbis-vorholt.ethz.ch/"
        openbis_instance = Openbis(
            url=base_url,
            verify_certificates=False,
            allow_http_but_do_not_use_this_in_production_and_only_within_safe_networks=True
        )
        token = openbis_instance.login('admin', 'changeit')
        # openbis_instance.set_token('dariza-230809113908224x25976BA0BCE4C7688F017A7365ABD456')
        # print(token)
        return openbis_instance

    o = get_instance()

    time.strftime("%Y-%M-%d_%H-%m-%S")

    ds_new = o.new_dataset(
        type='RAW_DATA',
        # type='PROCESSED_DATA',
        # experiment="/DEFAULT/DEFAULT/DEFAULT_EXP_2",
        sample='/DEFAULT/DEFAULT/EXP2',
        # object='/DEFAULT/DEFAULT/EXP1',
        # object='/DEFAULT/DEFAULT/S164',
        # sample='/DEFAULT/DEFAULT/DEFAULT/EXP4',
        # sample='/DEFAULT/DEFAULT/SAMPLE-3',
        props={'$name': "name_" + time.strftime("%Y-%M-%d_%H-%m-%S")},
        files = [
                # '/home/alaskowski/Downloads/test.txt',
                 # '/home/alaskowski/Downloads/testfile.txt',
                 # '/home/alaskowski/Downloads/upload_test/test_20M.txt',
                # '/home/alaskowski/Downloads/upload_test/upload_test2/upload_test3'
                '/home/alaskowski/Downloads/upload_test/upload_test2'
                 ])
    try:
        ds_new.save()
        print(ds_new.permId)
    except ValueError as v:
        print(v)






def test_multi_value_2():
    from pybis import Openbis
    def get_instance():
        base_url = "http://localhost:8888/openbis"
        base_url = "https://alaskowski:8443/openbis"
        # base_url = "https://openbis-sis-ci-sprint.ethz.ch/"
        openbis_instance = Openbis(
            url=base_url,
            verify_certificates=False,
            allow_http_but_do_not_use_this_in_production_and_only_within_safe_networks=True
        )
        token = openbis_instance.login('admin', 'changeit')
        print(token)
        return openbis_instance

    o = get_instance()
    name_suffix = str(time.time())

    types = o.get_property_types()

    property_type_code = "test_property_type_" + name_suffix
    # property_type_code = "MULTI-INTEGER"
    # pt_date = o.new_property_type(
    #     code=property_type_code,
    #     label='custom INTEGER property',
    #     description='custom property created in unit test',
    #     dataType='INTEGER',
    # )
    # pt_date.save()
    # time.sleep(1)
    # pt_date.delete('REASON')
    #
    # try:
    #     pt2 = o.get_property_type(property_type_code.lower())
    #     print("DUPA")
    # except ValueError as e:
    #     print(e)

    # obj_ebsdsim_software = o.new_object_type(
    #     code=property_type_code,
    #     generatedCodePrefix='EBSDSIM_SOFTWARE',
    #     # description         = 'Software used in EBSD Simulation',
    #     autoGeneratedCode=True
    # )
    # obj_ebsdsim_software.save()
    #
    # obj_ebsdsim_software.description = 'aaa'
    # obj_ebsdsim_software.save()

    # expt = o.new_experiment_type(code="EXP_" + property_type_code,
    #                                 description="my exciting new experiment")
    # expt.save()
    #
    # expt.description = 'aaa'
    # expt.save()

    # expt = o.new_dataset_type(code="EXP_" + property_type_code,
    #                                 description="my exciting new experiment")
    # expt.save()
    #
    # expt.description = 'aaa'
    # expt.save()


    # aa = o.get_samples(attrs=['parents', 'children'])[51].get_children()
    # cc = aa.get_children()
    a = o.get_samples()[50]
    c = a.get_children()

    print("DONE")

# executeCustomDSSService

def test_dss_service():
    from pybis import Openbis
    def get_instance():
        base_url = "http://localhost:8888/openbis"
        # base_url = "https://alaskowski:8443/openbis"
        # base_url = "https://openbis-sis-ci-sprint.ethz.ch/"
        openbis_instance = Openbis(
            url=base_url,
            verify_certificates=False,
            allow_http_but_do_not_use_this_in_production_and_only_within_safe_networks=True
        )
        token = openbis_instance.login('admin', 'changeit')
        print(token)
        return openbis_instance

    o = get_instance()
    name_suffix = str(time.time())

    response = o.executeCustomDSSService("imaging")
    # response2 = o.executeCustomDSSService("pingpong", "PINGP")
    # response = o.executeCustomASService("my-custom-service")

    print("DONE")


def test_dss_service2():
    from pybis import Openbis
    def get_instance():
        # base_url = "http://localhost:8888/openbis"
        base_url = "https://alaskowski:8443/openbis"
        # base_url = "https://openbis-sis-ci-sprint.ethz.ch/"
        # base_url = "https://openbis-vorholt.ethz.ch/"
        openbis_instance = Openbis(
            url=base_url,
            verify_certificates=False,
            allow_http_but_do_not_use_this_in_production_and_only_within_safe_networks=True
        )
        token = openbis_instance.login('admin', 'changeit')
        print(token)




        return openbis_instance

    token = '$pat-brast-231003165256434xDB681672497F6C892A4A6D89078EA6C5'

    token = '$pat-admin-231016140137705x0E1E1DB72289F7BE296E3714DF415365'

    token = '$pat-admin-231018111900142x3F3241496C9CF239D6742FF03657F321'

    # o = get_instance()
    o = Openbis(
        # url='https://openbis-vorholt.ethz.ch/',
        # url='https://openbis-sis-ci-sprint.ethz.ch/',
        url='https://alaskowski:8443/openbis',
        verify_certificates=False,
        # allow_http_but_do_not_use_this_in_production_and_only_within_safe_networks=True
    )
    o.set_token(token)

    name_suffix = str(time.time())

    # space = o.get_space('JUANF_TEST')
    # object_props = { '$name': "aaaaa"}
    # space = o
    # object = space.new_sample(type='JUAN_TEST',
    #                           code= 'RANDOM-' + name_suffix,
    #                           experiment = '/JUANF_TEST/JUAN_TEST_PROJECT/23JF01',
    #                           parents = ['/JUANF_TEST/JUAN_TEST_PROJECT/RANDOM1'],
    #                           props = object_props)

    space = o.get_space('DEFAULT')
    object_props = {'str': "bbbbbbb"}
    space = o
    object = space.new_sample(type='MY_OBJ',
                              code='RANDOM-' + name_suffix,
                              experiment='/DEFAULT/DEFAULT/DEFAULT',
                              parents=['/DEFAULT/DEFAULT/RANDOM-1697621201.0096185'],
                              children=['20231018112837761-58'],
                              props=object_props)


    object.save()


    print("DONE")

def test_dss_service23():
    from pybis import Openbis
    def get_instance():
        base_url = "http://localhost:8888/openbis"
        base_url = "https://alaskowski:8443/openbis"
        # base_url = "https://openbis-sis-ci-sprint.ethz.ch/"
        # base_url = "https://openbis-vorholt.ethz.ch/"
        openbis_instance = Openbis(
            url=base_url,
            verify_certificates=False,
            allow_http_but_do_not_use_this_in_production_and_only_within_safe_networks=True
        )
        token = openbis_instance.login('admin', 'changeit')
        print(token)

        return openbis_instance

    o = get_instance()
    name_suffix = str(time.time())

    # ds = o.get_datasets("20231023164722664-32")[0]
    # aa = ds
    # o.new_space()
    # o.new_project()

    project = o.get_project('/DEFAULT/DEFAULT')
    exp = o.new_experiment(code='MY_EXP_2',
                        type = 'DEFAULT_EXPERIMENT',
                        project = '/DEFAULT/DEFAULT'
                        )
    exp.save()



def test_del_terms():
    from pybis import Openbis
    def get_instance():
        base_url = "http://localhost:8888/openbis"
        base_url = "https://alaskowski:8443/openbis"
        base_url = "https://openbis-sis-ci-sprint.ethz.ch/"
        openbis_instance = Openbis(
            url=base_url,
            verify_certificates=False,
            allow_http_but_do_not_use_this_in_production_and_only_within_safe_networks=True
        )
        token = openbis_instance.login('admin', 'changeit')
        print(token)
        return openbis_instance

    o = get_instance()
    name_suffix = str(time.time())


    vocab = o.get_vocabulary('new_vocab')

    term = o.get_term('TERM7', 'NEW_VOCAB')

    term.delete('some_reason')


    print("DONE")


