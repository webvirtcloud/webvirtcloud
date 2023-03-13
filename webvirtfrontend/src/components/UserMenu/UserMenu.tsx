import ArrowLeftOnRectangleIcon from '@heroicons/react/20/solid/ArrowLeftOnRectangleIcon';
import ChevronUpDownIcon from '@heroicons/react/20/solid/ChevronUpDownIcon';
import Cog6ToothIcon from '@heroicons/react/20/solid/Cog6ToothIcon';
import { useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import tw from 'twin.macro';

import type { Profile } from '@/api/account';

import { Button } from '../Button';
import { Menu, MenuItem } from '../Menu';

type Props = {
  profile: Profile | undefined;
};

const UserMenu = ({ profile }: Props): JSX.Element => {
  const ref = useRef<HTMLDivElement>(null);
  const reference = useRef<HTMLButtonElement>();
  const [isOpen, toggle] = useState(false);
  const navigate = useNavigate();

  const handleLogout = () => {
    window.localStorage.removeItem('token');

    navigate('/sign-in');
  };

  const goToSettings = () => {
    navigate('/settings/');

    toggle(false);
  };

  return (
    <div ref={ref}>
      <Button
        ref={reference}
        variant="secondary"
        endIcon={<ChevronUpDownIcon width={16} height={16} />}
        onClick={() => toggle(!isOpen)}
      >
        <div css={tw`min-w-0 overflow-hidden max-w-[168px]`}>
          <h4 css={tw`font-bold truncate`}>{profile?.email}</h4>
        </div>
      </Button>
      <Menu
        isOpen={isOpen}
        source={reference}
        placement="bottom-end"
        onClose={() => toggle(false)}
      >
        <MenuItem
          startIcon={<Cog6ToothIcon width={16} height={16} />}
          onClick={() => goToSettings()}
        >
          Settings
        </MenuItem>
        <MenuItem
          startIcon={<ArrowLeftOnRectangleIcon width={16} height={16} />}
          onClick={() => handleLogout()}
        >
          Logout
        </MenuItem>
      </Menu>
    </div>
  );
};

export default UserMenu;
