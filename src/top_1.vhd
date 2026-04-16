library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity top_1 is

generic ( 
  c_clk_freq : integer := 100_000_000;
  c_baudrate : integer := 115_200
);

  Port ( 
        clk         : in std_logic;
        rx_i        : in std_logic;
        leds_o      : out std_logic_vector(3 downto 0)
        );
end top_1;

architecture Behavioral of top_1 is

component uart_rx is
generic ( 
  c_clk_freq : integer := 100_000_000;
  c_baudrate : integer := 115_200
);
    Port ( clk            : in STD_LOGIC;
           rx_i           : in STD_LOGIC;
           dout_o         : out std_logic_vector(7 downto 0);
           rx_done_tick_o : out STD_LOGIC);
end component;

signal led_i        : std_logic_vector(3 downto 0) := (others => '0');
signal dout         : std_logic_vector(7 downto 0) := (others => '0');
signal rx_done_tick : std_logic := '0';
--signal temp         : unsigned(7 downto 0);                                                      
--signal rx_done_d    : std_logic := '0'; -- önceki değer saklamak için                            
--                                                                                                 
--signal last_led : std_logic_vector(3 downto 0) := (others => '0');           -- SONRADAN EKLEME !

begin

i_uart_rx : uart_rx
generic map ( 
  c_clk_freq => c_clk_freq,
  c_baudrate => c_baudrate
)
Port map ( 
  clk            => clk,
  rx_i           => rx_i,
  dout_o         => dout,
  rx_done_tick_o => rx_done_tick
);

P_MAIN: process(clk)
begin
  if rising_edge(clk) then

     if (rx_done_tick = '1') then
     
            led_i <= dout(3 downto 0);      -- TERMİNALDEN SAYILARI HEX OLARAK GÖNDERİP TEST ETMELİSİN.        
     else
            led_i <= led_i;
     end if;
  end if;

end process;

leds_o <= led_i;

end Behavioral;