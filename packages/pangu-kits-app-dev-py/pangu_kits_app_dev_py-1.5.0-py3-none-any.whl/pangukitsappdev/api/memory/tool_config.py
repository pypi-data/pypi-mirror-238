#  Copyright (c) Huawei Technologies Co., Ltd. 2023-2023. All rights reserved.
from pangukitsappdev.api.common_config import ServerInfo


class ServerInfoTool(ServerInfo):

    def get_urls(self) -> [str]:
        return self.get_http_urls()
