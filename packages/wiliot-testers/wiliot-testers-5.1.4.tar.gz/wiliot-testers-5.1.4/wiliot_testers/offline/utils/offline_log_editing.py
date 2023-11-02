import pandas as pd
import time


def get_last_pass_external_id(packet_data_path):
    df_packet = pd.read_csv(packet_data_path)
    last_location = max(df_packet[df_packet['status_offline'] == 1]['tag_run_location'])
    external_id = df_packet[df_packet['tag_run_location'] == last_location]['external_id'].unique()
    if len(external_id) != 1:
        raise Exception(f'Could not extract last external id since external id is not specified or several external ids'
                        f' on the same location: {external_id}')
    return external_id[0]


def delete_entry_from_specific_external_id(packet_data_path, run_data_path, external_id, new_file_suffix='_edit'):
    df_packet = pd.read_csv(packet_data_path)
    df_run = pd.read_csv(run_data_path)

    i_to_remove = df_packet[df_packet['external_id'] == external_id].index
    if len(i_to_remove) == 0:
        raise Exception('could not find the specifies external id')
    df_packet_edit = df_packet.drop(list(range(min(i_to_remove), len(df_packet))))
    df_run['total_run_tested'] = max(df_packet_edit['tag_run_location']) + 1
    df_run['total_run_passed_offline'] = \
        len(df_packet_edit[df_packet_edit['status_offline'] == 1]['tag_run_location'].unique())
    df_run['total_run_responding_tags'] = len(df_packet_edit['adv_address'].unique())
    cur_comments = df_run['comments'][0] if not pd.isnull(df_run['comments'][0]) else ''
    last_external_id = get_last_pass_external_id(packet_data_path)
    df_run['comments'] = cur_comments + f'.del:{external_id[-4:]}-{last_external_id[-4:]}' \
                                        f'@{time.strftime("%d%m%y_%H%M%S")}'
    packet_data_path = packet_data_path.replace('.CSV', '.csv')
    run_data_path = run_data_path.replace('.CSV', '.csv')
    df_packet_edit.to_csv(packet_data_path.replace('.csv', f'{new_file_suffix}.csv'), index=False)
    df_run.to_csv(run_data_path.replace('.csv', f'{new_file_suffix}.csv'), index=False)
    return df_run


if __name__ == '__main__':
    FILE_PATH = 'C:/Users/shunit/eclipse-workspace/post_process_testing/offline/duplication1'
    commmon_run_name = '02jx_20221224_203102'
    packet_data_path = f"{FILE_PATH}/{commmon_run_name}@packets_data.csv"
    run_data_path = f"{FILE_PATH}/{commmon_run_name}@run_data.csv"

    last_external_id = get_last_pass_external_id(packet_data_path)
    print(last_external_id)

    external_id_to_delete = last_external_id
    new_df = delete_entry_from_specific_external_id(packet_data_path, run_data_path,
                                                    external_id=external_id_to_delete, new_file_suffix='_edit')
    print('done')
