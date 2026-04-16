
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;


entity uart_rx is


generic ( 
  c_clk_freq : integer          := 100_000_000;
  c_baudrate : integer          := 115_200
);
    Port ( clk                      : in STD_LOGIC;
           rx_i                     : in STD_LOGIC;
           dout_o                   : out std_logic_vector (7 downto 0);
           rx_done_tick_o           : out STD_LOGIC);
end uart_rx;

architecture Behavioral of uart_rx is

constant c_bittimerlim : integer                := c_clk_freq/c_baudrate;           -- T kadar süre demek   "8.68 us"
                                                                                    -- Receiver iletimde bizim ihtiyacımız olan T/2.
type states is (IDLE, START, DATA, STOP);
signal state : states := IDLE;

signal bittimer: integer range 0 to c_bittimerlim   := 0;
signal bitcnt : integer range 0 to 7 := 0;
signal shift_reg : std_logic_vector(7 downto 0)         :=  (others => '0');
    
begin

    P_MAIN: process(clk)
    begin
            if (rising_edge(clk)) then
                case state is
                    
                    when IDLE =>
                    
                        rx_done_tick_o      <= '0';
                        bittimer            <= 0;
                            if (rx_i = '0') then                                -- RX_İ BİTİ RECEİVERDA HER ZAMAN BASLANGIÇTA 1 OLARAK BEKLER 0 GELDİĞİ ANDA START BİTİNİ AKTİF EDER.(BURASI DÜZELTİLDİ.)
                            state <= START;
                            end if;
                            
                    when START => 
                        
                        if (bittimer =  c_bittimerlim/2 - 1) then
                        state        <= DATA;
                        bittimer     <= 0;
                        else
                        bittimer     <= bittimer + 1;
                        end if;
                        
                    when DATA =>
                        if (bittimer = c_bittimerlim - 1) then
                            if (bitcnt = 7) then
                                state    <= STOP;
                                bitcnt   <= 0;
                            else
                                bitcnt   <= bitcnt + 1;                           
                            end if;  
                            
                          shift_reg          <=  rx_i & (shift_reg (7 downto 1));                   -- BURADA REGİSTER İŞLEMİ YAPILIR. YENİ GELEN BİT DEĞERİ BİNARY OLARAK TOPLAM DEĞERİN EN SOLUNA YAZILIR.
                          bittimer       <= 0;  
                         else  
                          bittimer       <= bittimer + 1;                  
                        end if;
                    
                    when STOP =>
                        if (bittimer      =  c_bittimerlim - 1) then
                        state            <= IDLE;
                        bittimer         <= 0;
                        rx_done_tick_o   <= '1';
                        
                        else
                        bittimer         <= bittimer + 1;
                        end if;
                end case;
            end if;
    end process P_MAIN;
    
dout_o <= shift_reg;

end Behavioral;
