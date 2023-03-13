import { useAtomValue } from 'jotai';
import { Link, NavLink } from 'react-router-dom';
import tw from 'twin.macro';

import { Console, ServerList, Settings } from '@/components/Icons';
// import ProjectSelector from '@/components/ProjectSelector';
import UserMenu from '@/components/UserMenu';
import { useProfileStore } from '@/store/profile';

const Navbar = (): JSX.Element => {
  const profile = useAtomValue(useProfileStore);

  const links: { to: string; name: string }[] = [
    { to: `/servers`, name: 'Virtances' },
    { to: `/keypairs`, name: 'Keypairs' },
    { to: `/settings`, name: 'Settings' },
  ];

  return (
    <nav
      css={tw`sticky top-0 left-0 right-0 z-10 flex flex-col justify-between border-b shadow-sm bg-base border-black/10`}
    >
      <div css={tw`container p-4 mx-auto`}>
        <div css={tw`flex items-center justify-between`}>
          <div css={tw`flex items-center mb-4 space-x-4`}>
            <Link css={tw`inline-flex items-center justify-center space-x-4`} to="/">
              <img
                css={tw`w-8`}
                src={new URL('/src/assets/images/logo.svg', import.meta.url).href}
                alt="Logotype"
              />
            </Link>
            <div css={tw`w-px h-6 bg-alt2`}></div>
            {/* <ProjectSelector /> */}
          </div>
          <UserMenu profile={profile} />
        </div>

        <ul css={tw`flex items-center space-x-2`}>
          {links.map((link) => (
            <li key={link.name}>
              <NavLink to={link.to}>
                {({ isActive }) => (
                  <span
                    css={[
                      tw`w-full inline-flex items-center space-x-2 rounded-md transition-opacity px-2 py-1.5`,
                      isActive
                        ? tw`bg-interactive-hover`
                        : tw`opacity-50 hover:opacity-100`,
                    ]}
                  >
                    {link.name === 'Virtances' && <ServerList width={18} height={18} />}
                    {link.name === 'Keypairs' && <Console width={18} height={18} />}
                    {link.name === 'Settings' && <Settings width={18} height={18} />}
                    <span css={tw`font-semibold`}>{link.name}</span>
                  </span>
                )}
              </NavLink>
            </li>
          ))}
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
