import { useNavigate } from 'react-router-dom';
import useSWR from 'swr';
import tw from 'twin.macro';

import type { Server } from '@/api/servers';
import { getServers } from '@/api/servers';
import { Button } from '@/components/Button';
import Input from '@/components/Input';

import ServerItem from './ServerItem';

interface Props {
  servers: Server[] | undefined;
}

const ServersList = ({ servers }: Props): JSX.Element => {
  const navigate = useNavigate();

  return (
    <section>
      <div css={tw`flex items-center justify-between mb-8`}>
        <h2 css={tw`text-xl font-bold`}>Servers List</h2>
        <div css={tw`flex items-center space-x-2`}>
          <Button onClick={() => navigate('/servers/create')} size="md">
            Create server
          </Button>
          <Input id="server-search" name="server-search" placeholder="Search..." />
        </div>
      </div>

      {servers ? (
        <ul css={tw`grid gap-4 md:grid-cols-2 xl:grid-cols-3`}>
          {servers.map((server) => (
            <li key={server.uuid}>
              {<ServerItem to={`/servers/${server.uuid}`} server={server} />}
            </li>
          ))}
        </ul>
      ) : (
        <div>Loading...</div>
      )}
      {servers && servers.length === 0 && <div>No created servers.</div>}
    </section>
  );
};

const Servers = (): JSX.Element => {
  const { data } = useSWR('/servers/', getServers);

  return (
    <main>
      <ServersList servers={data ? data.servers : undefined} />
    </main>
  );
};

export default Servers;
