import { useState } from 'react';
import useSWR from 'swr';
import tw from 'twin.macro';

import { type Keypair, deleteKeypair, getKeypairs } from '@/api/keypairs';
import { Button } from '@/components/Button';
import { CreateKeypairDialog } from '@/components/Dialogs/CreateKeypair';

import { KeypairsTable } from './KeypairsTable';

export default function Keypairs() {
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);

  const { data, mutate, error } = useSWR('/keypairs/', getKeypairs);

  const onCreate = (keypair: Keypair) => {
    mutate({ keypairs: data ? [keypair, ...data.keypairs] : [] });
  };

  const onUpdate = (keypair: Keypair) => {
    mutate({
      keypairs: data
        ? data.keypairs.map((key) => (key.id === keypair.id ? keypair : key))
        : [],
    });
  };

  const onDelete = (id: number) => {
    return deleteKeypair(id).then(() => {
      mutate({ keypairs: data ? data.keypairs.filter((key) => key.id !== id) : [] });
    });
  };

  return (
    <div>
      <div css={tw`flex items-center justify-between mb-8`}>
        <h2 css={tw`text-xl font-bold`}>Keypairs</h2>
        <Button onClick={() => setIsCreateDialogOpen(true)}>Create Keypair</Button>
        <CreateKeypairDialog
          isOpen={isCreateDialogOpen}
          onToggle={setIsCreateDialogOpen}
          onCreate={onCreate}
        />
      </div>

      <KeypairsTable data={data} error={error} onUpdate={onUpdate} onDelete={onDelete} />
    </div>
  );
}
