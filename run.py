import SentinelUtils
import dateutil
import SentinelAzure

"""
class read(object):
    result = SentinelUtils.ConfigReader.read_config_values('C:\\Users\\zhzhao\\source\\repos\\PythonSDK\\PythonSDK\\json_parser\\asi_config.json')
    print(result)

class check(object):
    check = SentinelUtils.version_management.ModuleVersionCheck()
    result = check.validate_python('3.6.0')
    print(result)
    result = check.validate_installed_modules(['Kqlmagic>=0.1.92', 'pip>=9.0.2'])

    print(result[1].requirement_met)
    print(result[1].name)

class azure_snapshot(object):
    resource_group = 'PIOnDemand'
    vm_name = 'PIODDemoWin2k16'
    user_id = 'pitester@M365x387926.onmicrosoft.com'
    password = 'NextBigThing@511'
    subscription_id = '0cd2d516-2b4d-4aea-8e62-e6cd8f9a78c6'

    auth = SentinelAzure.azure_aad_helper.AADHelper()
    compute_client, network_client, resource_client, storage_client = auth.authenticate('User ID Password', **{'user_id': user_id, 'password' : password, 'subscription_id' : subscription_id})
    comp = SentinelAzure.azure_compute_helper.ComputeHelper(compute_client, resource_group)
    disk_list = comp.get_vm_disk_names(vm_name)
    if disk_list is not None and len(disk_list) > 0:
        result = comp.create_snapshot_async(**{'snapshot_name' : 'my_test_snapshot1', 'selected_disk' : disk_list[0]})
        if result is not None and result.provisioning_state == 'Succeeded':
            sas_url = comp.generate_snapshot_sas_url_async(**{'snapshot_name' : 'my_test_snapshot1', 'int_seconds' : 360000})
            print(sas_url)

class azure_pi(object):
    resource_group = 'PIOnDemand'
    vm_extension_name = 'sentinelmemoryinvestigator'
    storage_account_name = 'zzpytest'
    storage_location = 'westus2'
    blob_container_name = 'memorydumpfolder'
    user_id = 'pitester@M365x387926.onmicrosoft.com'
    password = 'NextBigThing@511'
    subscription_id = '0cd2d516-2b4d-4aea-8e62-e6cd8f9a78c6'

    #os_type = 'Windows'
    os_type = 'Linux'

    if os_type == 'Windows':
        vm_name = 'PIODDemoWin2k16'
        vm_location = 'westus2'
        file_list = ['https://pinotebookresults.blob.core.windows.net/results/installNotebookExtension.ps1?sp=r&st=2019-03-28T21:34:09Z&se=2019-06-01T05:34:09Z&spr=https&sv=2018-03-28&sig=83jlp%2Fr%2BVcuGRLRij6jssqMerCgkk2pp0s007sLUPpM%3D&sr=b', 'https://pinotebookresults.blob.core.windows.net/results/piextension.zip?sp=r&st=2019-03-28T21:44:08Z&se=2019-06-01T05:44:08Z&spr=https&sv=2018-03-28&sig=UoBRXLRK9C4xurBjYu%2FkqqlkjCSi%2B3FlmFiWcsqlu6E%3D&sr=b']
    elif os_type == 'Linux':
        vm_name = 'PIODDemoLinux'
        vm_location = 'eastus'
        file_list = ['https://pilinuxstorage.blob.core.windows.net/release/ondemand/latest/piondemand.sh?sp=r&st=2019-03-26T18:25:43Z&se=2019-08-24T02:25:43Z&spr=https&sv=2018-03-28&sig=Cd89A/kt3Yjwx64Sk2l6rKMDQmdDaH1AX/WBfpH7D70=&sr=b','https://pilinuxstorage.blob.core.windows.net/release/ondemand/latest/pilinux.ondemand.tar.bz2?sp=r&st=2019-03-26T18:24:54Z&se=2019-07-20T02:24:54Z&spr=https&sv=2018-03-28&sig=nNJHV8ESXXZQXV/1BO4TGaagdINWaZGo/f6Kxh2QGd0=&sr=b']

    # initialize Azure clients
    auth = SentinelAzure.azure_aad_helper.AADHelper()
    compute_client, network_client, resource_client, storage_client = auth.authenticate('User ID Password', **{'user_id': user_id, 'password' : password, 'subscription_id' : subscription_id})
    
    # create a blob storage for uploading
    stor = SentinelAzure.azure_storage_helper.StorageHelper(storage_client)

    name_availability = stor.is_storage_account_name_available(storage_account_name)
    if name_availability.name_available == False:
        print('Name is already used, please provide a different name')

    #storage_creation = stor.create_storage_account_async(storage_account_name, resource_group, **{'storage_location' : storage_location})
    storage_list = stor.get_storage_account_names(resource_group)
    print(len(storage_list))

    storage_key = stor.get_storage_account_key(storage_account_name, resource_group)

    stor.initialize_block_blob_service(storage_account_name, storage_key, blob_container_name)
    #blob_conteiner = stor.create_blob_container()

    check_blob = stor.get_blob_container()

    sas_url = stor.generate_blob_container_sas_url(100)
    upload_container_path = stor.build_upload_container_path(os_type, sas_url)

    # VM Extension work
    if os_type == 'Windows':
        command_to_execute = 'powershell -File installNotebookExtension.ps1 "{0}" >> out.txt'.format(upload_container_path)
        vm_extension_properties = SentinelAzure.WindowsVMExtensionProperties(command_to_execute, file_list)
    elif os_type == 'Linux':
        command_to_execute = './piondemand.sh "' + upload_container_path + '"'
        vm_extension_properties = SentinelAzure.LinuxVMExtensionProperties(command_to_execute, file_list)
    
    comp = SentinelAzure.azure_compute_helper.ComputeHelper(compute_client, resource_group)
    vm_extension = comp.initialize_vm_extension(vm_extension_properties, vm_location)
    result = comp.create_vm_extension_async(vm_name, vm_extension_name, vm_extension)
    returned_json = comp.get_uploaded_result(upload_container_path)

    del_result = comp.delete_vm_extension_async(vm_name, vm_extension_name)

class azure_windows_vm_with_vhd_explorer(object):
    resource_group = 'fng'
    resource_group_location = 'centralus'
    vm_name = 'fntools'
    storage_account_name = 'zzpytestvhd'
    blob_container_name = 'vmimage'
    user_id = 'pitester@M365x387926.onmicrosoft.com'
    password = 'NextBigThing@511'
    vm_user_id = 'zhzhao'
    vm_password = 'Twoboys!8888'
    subscription_id = '0cd2d516-2b4d-4aea-8e62-e6cd8f9a78c6'
    os_type = 'Windows'
    file_name = 'abcd.vhd'
    file_path = 'https://md-fgbzgtg0clff.blob.core.windows.net/z30cbwmnszkt/abcd?sv=2017-04-17&sr=b&si=b22b27b8-8b20-4ec3-ba23-8b02d0f84dc7&sig=XT6ol1DqNnzKpV3myCqqUrrT8INr%2F336zE9Lsi5yoRc%3D'
    nic_name = 'mytestnic'
    snapshot_name = 'mytestsnapshot'

    # initialize Azure clients
    auth = SentinelAzure.azure_aad_helper.AADHelper()
    compute_client, network_client, resource_client, storage_client = auth.authenticate('User ID Password', **{'user_id': user_id, 'password' : password, 'subscription_id' : subscription_id})
    
    # resource management
    rm = SentinelAzure.azure_resource_helper.ResourceHelper(resource_client, resource_group)
    result = rm.create_resource_group(resource_group_location)

    # create a blob storage for uploading
    stor = SentinelAzure.azure_storage_helper.StorageHelper(storage_client)

    name_availability = stor.is_storage_account_name_available(storage_account_name)
    if name_availability.name_available == False:
        print('Name is already used, please provide a different name')

    storage_creation = stor.create_storage_account_async(storage_account_name, resource_group, **{'storage_location' : resource_group_location})
    storage_list = stor.get_storage_account_names(resource_group)
    print(len(storage_list))

    storage_key = stor.get_storage_account_key(storage_account_name, resource_group)

    stor.initialize_block_blob_service(storage_account_name, storage_key, blob_container_name)
    blob_conteiner = stor.create_blob_container()
    check_blob = stor.get_blob_container()

    sas_url = stor.copy_vhd(file_name, file_path)

    # Network
    net = SentinelAzure.azure_network_helper.NetworkHelper(network_client, nic_name)
    net.prepare_network_for_vm_creation(resource_group, resource_group_location)
    nic = net.get_nic(resource_group)

    # VM work
    comp = SentinelAzure.azure_compute_helper.ComputeHelper(compute_client, resource_group)
    result = comp.create_vm(nic, **{'vm_location' : resource_group_location, 'user_name' : vm_user_id, 'password' : vm_password, 'vm_name' : vm_name, 'snapshot_name' : snapshot_name, 'os_type' : os_type, 'stroage_account_name' : storage_account_name, 'blob_container_name' : blob_container_name})

    # last step
    del_result = comp.delete_vm_async(vm_name)

class azure_windows_vm_creation(object):
    resource_group = 'fng'
    resource_group_location = 'centralus'
    vm_name = 'fntools'
    storage_account_name = 'zzpytestvhd'
    blob_container_name = 'vmimage'
    user_id = 'pitester@M365x387926.onmicrosoft.com'
    password = 'NextBigThing@511'
    vm_user_id = 'zhzhao'
    vm_password = 'Twoboys!8888'
    subscription_id = '0cd2d516-2b4d-4aea-8e62-e6cd8f9a78c6'
    os_type = 'Windows'
    file_name = 'abcd.vhd'
    file_path = 'https://md-fgbzgtg0clff.blob.core.windows.net/z30cbwmnszkt/abcd?sv=2017-04-17&sr=b&si=b22b27b8-8b20-4ec3-ba23-8b02d0f84dc7&sig=XT6ol1DqNnzKpV3myCqqUrrT8INr%2F336zE9Lsi5yoRc%3D'
    nic_name = 'mytestnic'
    snapshot_name = 'mytestsnapshot'

    # initialize Azure clients
    auth = SentinelAzure.azure_aad_helper.AADHelper()
    compute_client, network_client, resource_client, storage_client = auth.authenticate('User ID Password', **{'user_id': user_id, 'password' : password, 'subscription_id' : subscription_id})
    
    
    # create a blob storage for uploading
    stor = SentinelAzure.azure_storage_helper.StorageHelper(storage_client)

    storage_creation = stor.create_storage_account_async(storage_account_name, resource_group, **{'storage_location' : resource_group_location})
    storage_list = stor.get_storage_account_names(resource_group)


    storage_key = stor.get_storage_account_key(storage_account_name, resource_group)

    stor.initialize_block_blob_service(storage_account_name, storage_key, blob_container_name)
    
    check_blob = stor.get_blob_container()

   

    # Network
    net = SentinelAzure.azure_network_helper.NetworkHelper(network_client, nic_name)
    
    nic = net.get_nic(resource_group)

    # VM work
    comp = SentinelAzure.azure_compute_helper.ComputeHelper(compute_client, resource_group)
    result = comp.create_vm(nic, **{'vm_location' : resource_group_location, 'user_name' : vm_user_id, 'password' : vm_password, 'vm_name' : vm_name, 'snapshot_name' : snapshot_name, 'os_type' : os_type, 'stroage_account_name' : storage_account_name, 'blob_container_name' : blob_container_name})

    # last step
    del_result = comp.delete_vm_async(vm_name)

"""

class azure_aad(object):
    resource_group = 'PIOnDemand'
    vm_name = 'PIODDemoWin2k16'
    user_id = 'pitester@M365x387926.onmicrosoft.com'
    password = 'NextBigThing@511'
    subscription_id = '0cd2d516-2b4d-4aea-8e62-e6cd8f9a78c6'

    auth = SentinelAzure.azure_aad_helper.AADHelper()
    compute_client, network_client, resource_client, storage_client = auth.authenticate('CLI based', **{'user_id': user_id, 'password' : password, 'subscription_id' : subscription_id})
    comp = SentinelAzure.azure_compute_helper.ComputeHelper(compute_client, resource_group)
    disk_list = comp.get_vm_disk_names(vm_name)
